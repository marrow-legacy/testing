# encoding: utf-8

from __future__ import unicode_literals, print_function

import copy

from marrow.util.bunch import Bunch
from marrow.util.compat import exception

from functools import partial
from concurrent import futures


__all__ = ["Feature"]

log = __import__('logging').getLogger(__name__)



class Step(object):
    def __init__(self, fn, description, kind=None):
        super(Step, self).__init__()
        
        self.registry = Bunch(
                scenario = [],
                given = [],
                when = [],
                then = []
            )
        
        self.fn = fn
        self.description = description
        
        self.kind = kind if kind else self.__class__.__name__
    
    def __call__(self, environ=None):
        if environ is None:
            environ = Bunch()
        
        if self.fn:
            result = self.fn(environ)
            if result:
                environ = result
        
        return environ
    
    def fast(self, environ, workers):
        messages = []
        
        try:
            environ = self(environ)
        except:
            messages.extend(("    " * self.indentation + " " * (len(self.kind) + 2) + i) for i in exception().formatted.split("\n") if i)
            return messages
        
        # Execute steps.
        jobs = {}
        messages = []
        executor = futures.ThreadPoolExecutor(max_workers=workers)
        
        for stage in ('scenario', 'given', 'when', 'then'):
            for next in self.registry[stage]:
                job = executor.submit(next.fast, copy.deepcopy(environ), workers)
                jobs[job] = next
        
        # Wait for sub-steps to complete and process results as they become available..
        for job in futures.as_completed(jobs):
            step = jobs[job]
            messages.append("%s%s: %s%s." % ('    ' * step.indentation, step.kind, step.description[0].upper(), step.description[1:]))
            messages.extend(job.result())
        
        return messages
    
    def chain(self):
        chains = []
        
        for stage in ('scenario', 'given', 'when', 'then'):
            for next in self.registry[stage]:
                for chain in next.chain():
                    chains.append([self] + chain)
        
        if not chains:
            return [[self]]
        
        return chains


class Then(Step):
    indentation = 4
    
    def then(self, description):
        kind = ' And' if self.__class__ is Then else None
        
        def decorator(fn):
            obj = Then(fn, description, kind)
            self.registry.then.append(obj)
            return obj
        
        return decorator


class When(Then):
    indentation = 3
    
    def when(self, description):
        kind = ' And' if self.__class__ is When else None
        
        def decorator(fn):
            obj = When(fn, description, kind)
            self.registry.when.append(obj)
            return obj
        
        return decorator


class Given(When):
    indentation = 2
    
    def given(self, description):
        kind = '  And' if self.__class__ is Given else None
        
        def decorator(fn):
            obj = Given(fn, description, kind)
            self.registry.given.append(obj)
            return obj
        
        return decorator


class Scenario(Given):
    indentation = 1
    
    def scenario(self, description):
        kind = '     And' if self.__class__ is Scenario else None
        
        def decorator(fn):
            obj = Scenario(fn, description, kind)
            self.registry.scenario.append(obj)
            return obj
        
        return decorator


class Feature(Scenario):
    indentation = 0


class Suite(object):
    def __init__(self, prepost=None):
        self.features = []
        
        self.prepost = prepost
    
    def __call__(self, environ=None, workers=1, method='fast'):
        generator = None
        
        if environ is None:
            environ = Bunch()
        
        if self.prepost:
            generator = self.prepost(environ)
            generator.next()
        
        method = getattr(self, method)
        method(environ, workers)
        
        if generator:
            try:
                generator.next()
            except StopIteration:
                pass
    
    def feature(self, description):
        def decorator(fn):
            obj = Feature(fn, description)
            self.features.append(obj)
            return obj
        
        return decorator
    
    def fast(self, environ, workers):
        """Process each step as it is encountered.
        
        This has the issue that if what you are testing involves session state
        this runner may perform mutually exclusive operations in parallel as
        each step is only run once.  (E.g. nested actions operate on the same
        session.)
        
        This can be visualized thus: (each is run once)
        
        Feature A
            When A
                Then A
                Then B
            When B
                Then C
                Then D
        Feature B
            ...
        
        Each indentation level is executed in parallel.
        """
        
        # Execute features.
        jobs = {}
        executor = futures.ThreadPoolExecutor(max_workers=workers)
        
        for feature in self.features:
            job = executor.submit(feature.fast, environ, workers)
            jobs[job] = feature
        
        # Wait for sub-steps to complete and process results as they become available..
        for job in futures.as_completed(jobs):
            feature = jobs[job]
            print("%s%s: %s%s." % ("    " * feature.indentation, feature.kind, feature.description[0].upper(), feature.description[1:]))
            
            messages = job.result()
            
            print("\n".join(messages), end="\n\n")
    
    def chain(self, environ, workers):
        """Process steps top-to-bottom in a less efficient, but safer way.
        
        This builds "chains" of steps, specifically every combination from
        the Feature through Then.  This can be visualized thus:
        
        Feature A, When A, Then A
        Feature A, When A, Then B
        Feature A, When B, Then C
        Feature A, When B, Then D
        Feature B, ...
        
        Chains are executed in parallel.  This means, however, that if an
        intermediary step in the chain has an exception, the exception will
        be repeated for each chain!
        """
        
        jobs = []
        executor = futures.ThreadPoolExecutor(max_workers=workers)
        
        for feature in self.features:
            chains = feature.chain()
            
            # Execute features.
            for chain in chains:
                job = executor.submit(self.chain_, chain, copy.deepcopy(environ))
                jobs.append(job)
        
        # Wait for sub-steps to complete and process results as they become available..
        for job in futures.as_completed(jobs):
            messages = job.result()
            
            print("\n".join(messages), end="\n\n")
    
    def chain_(self, chain, environ):
        messages = []
        
        for fn in chain:
            messages.append("%s%s: %s%s." % ("    " * fn.indentation, fn.kind, fn.description[0].upper(), fn.description[1:]))
            try:
                environ = fn(environ)
            except:
                messages.extend(("    " * fn.indentation + " " * (len(fn.kind) + 2) + i) for i in exception().formatted.split("\n") if i)
                return messages
        
        return messages
    
    @classmethod
    def decorated(cls, fn):
        return cls(fn)
