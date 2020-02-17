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
        return (l[0] and r[0], max(l[1], r[1]))

class Or(BinaryOp):
    def eval(self, ctx):
        l = self.left.eval(ctx)
        r = self.right.eval(ctx)
        return (l[0] or r[0], min(l[1], r[1]))

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
        self.value = int(value)

    def eval(self, ctx):
        return self.value

class Regex():
    def __init__(self, exp):
        self.exp = "^" + exp
    
    def eval(self, ctx):
        match = re.search(self.exp, ctx.text[ctx.offset:])
        if match is None:
            return (False, 0)
        else:
            return (True, match.end())

class Compare(BinaryOp):
    def eval(self, ctx):
        return (self.left.eval(ctx) == self.right.eval(ctx), 0)

class Program():
    def __init__(self, rule, next_p):
        self.rule = rule
        self.next_p = next_p
    
    def eval(self, ctx):
        if ctx.offset in ctx.triggers:
            for to_exec in ctx.triggers[ctx.offset]:
                to_exec.eval(ctx)
        self.rule.eval(ctx)
        self.next_p.eval(ctx)

        return ctx.score

class Rule():
    def __init__(self, start, stop, store):
        self.start = start
        self.stop = stop
        self.store = store
    
    def eval(self, ctx):
        name = self.store.get_name()
        if not name in ctx.output:
            ctx.output[name] = ""

        if id(self) not in ctx.active:
            start = self.start.eval(ctx)
            if start[0]:
                if self.start.is_after():
                    ctx.active[id(self)] = ctx.offset + start[1]
                else:
                    ctx.active[id(self)] = ctx.offset

        if id(self) in ctx.active and ctx.offset >= ctx.active[id(self)]:
            if ctx.offset == ctx.active[id(self)]:
                ctx.changed = True
            
            diff = ctx.offset - ctx.active[id(self)]
            stop = self.stop.eval(ctx)
            if stop[0]:

                ctx.changed = True

                del ctx.active[id(self)]

                if self.stop.is_after():
                    ctx.output[name] += ctx.text[ctx.offset:ctx.offset + stop[1]]
                    self.store.eval(ctx)
                elif len(ctx.output[name]) > 0:
                    self.store.eval(ctx)
                return

            ctx.output[name] += ctx.text[ctx.offset]

class Weight():
    def __init__(self, weight, to_execute):
        self.weight = weight
        self.to_execute = to_execute
    def eval(self, ctx):
        ctx.score += self.weight.eval(ctx)
        ctx.matches += 1
        self.to_execute.eval(ctx)

class Conditional():
    def __init__(self, condition, delim_after, weight):
        self.condition = condition
        self.weight = weight
        self.delim = delim_after
        self.weight = weight
    
    def is_after(self):
        return self.delim
    
    def eval(self, ctx):
        res = self.condition.eval(ctx) 
        if res[0]:
            off = ctx.offset + res[1]
            if off not in ctx.triggers:
                ctx.triggers[off] = []
            
            ctx.triggers[off] += [self.weight]
        return res

class Force():
    def __init__(self, source, dest, conditional):
        self.source = source
        self.dest = dest
        self.conditional = conditional
    
    def eval(self, ctx):
        if self.conditional.eval(ctx)[0]:
            ctx.output[self.dest] = self.source

class BooleanCond():
    def __init__(self, val):
        self.val = val
    
    def eval(self, ctx):
        return (self.val, 0)

class Store():
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    
    def get_name(self):
        return self.name
    
    def eval(self, ctx):
        self.weight.eval(ctx)

class Init():
    def __init__(self, assigns):
        self.assigns = assigns
        self.done = False
    def eval(self, ctx):
        if not self.done:
            self.assigns.eval(ctx)
            self.done = True

class Nop():
    def __init__(self):
        pass
    def eval(self, ctx):
        pass