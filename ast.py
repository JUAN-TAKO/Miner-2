import re

class BinaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right

class UnaryOp():
    def __init__(self, right):
        self.right = right


class And(BinaryOp):
    def eval(self, ctx):
        l = self.left.eval(ctx)
        r = self.right.eval(ctx)
        return (l[0] and r[0], min(l[1], r[1]))

class Or(BinaryOp):
    def eval(self, ctx):
        l = self.left.eval(ctx)
        r = self.right.eval(ctx)
        return (l[0] or r[0], max(l[1], r[1]))

class Not(UnaryOp):
    def eval(self, ctx):
        r = self.right.eval(ctx)
        return (not r[0], r[1])

class Assign(BinaryOp):
    def eval(self, ctx):
        ctx.variables[self.left.get_name()] = self.right.eval(ctx)
        return 0

class AssignList():
    def __init__(self, assign, next_a):
        self.assign = assign
        self.next_a = next_a
    def eval(self, ctx):
        self.assign.eval(ctx)
        if self.next_a:
            self.next_a.eval(ctx)
        return 0

class Variable():
    def __init__(self, name):
        self.name = name
    def eval(self, ctx):
        return ctx.variables[self.name]
    def get_name(self):
        return self.name

class Number():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)

class Regex():
    def __init__(self, exp):
        self.exp = "^" + exp
    
    def eval(self, ctx):
        match = re.search(self.exp, ctx.text[ctx.offset:])
        return (not match is None, match.end())

class Compare(BinaryOp):
    def eval(self, ctx):
        return (self.left.eval(ctx) == self.right.eval(ctx), 0)

class Program():
    def __init__(self, rule, next_p):
        self.rule = rule
        self.next_p = next_p
    
    def eval(self, ctx):
        self.rule.eval(ctx)
        self.next_p.eval(ctx)

class Rule():
    def __init__(self, start=None, stop=None, store=None, once=None):
        self.start = start
        self.stop = stop
        self.store = store
        self.once = once
    
    def eval(self, ctx):
        pass

class Delimitation():
    def __init__(self, is_after):
        self.is_after = is_after
    
    def eval(self, ctx):
        return self.is_after


class Conditional():
    def __init__(self, condition, to_execute, delim):
        self.condition = condition
        self.to_execute = to_execute
        self.delim = delim
    
    def get_delim(self):
        return self.delim
    
    def eval(self, ctx):
        res = self.condition.eval(ctx) 
        if res[0]:
            self.to_execute.eval(ctx)
        return res

class Force():
    def __init__(self, source, dest, conditional):
        self.source = source
        self.dest = dest
        self.conditional = conditional
    
    def eval(self, ctx):
        if self.conditional.eval(ctx)[0]:
            ctx.output[self.dest]["value"] = self.source

class Store():
    def __init__(self, )