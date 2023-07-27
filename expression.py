from abc import abstractmethod, ABCMeta
import pandas as pd
# 抽象表达式接口，根据业务场景规范表达式
# 使用抽象类需要使用python3


class Expression(metaclass=ABCMeta):

    @abstractmethod
    def interpret(self, context):
        pass

# 构建变量表达式，或者叫终端表达式，其他表达式求值时通过层层追溯最后指向这里
# 变量与执行环境的Key对应，最终会通过key获取传入的值


class VarExpression(Expression):

    def __init__(self, key):
        Expression.__init__(self)
        self.key = key

    # 覆盖表达式，根据key获取变量
    def interpret(self, context):
        return context.get(self.key)


class SelectoneExpression(Expression):

    def __init__(self, df, expr_one):
        Expression.__init__(self)
        self.df = df
        self.expr_one = expr_one

    def interpret(self, context):
        dataframe = self.df.interpret(context)
        if self.expr_one.interpret(context) == "*":
            return dataframe
        if "+" in self.expr_one.interpret(context):
            return SelectaddExpression(self.df, self.expr_one).interpret(context)
        if "*" in self.expr_one.interpret(context):
            return SelectonemutipleExpression(self.df, self.expr_one).interpret(context)
        else:
            return dataframe[self.expr_one.interpret(context)]


class SelectaddExpression(Expression):

    def __init__(self, df, expr_one):
        Expression.__init__(self)
        self.df = df
        self.expr_one = expr_one

    def interpret(self, context):
        left, right = (self.expr_one.interpret(context).split("+"))
        # print(left, right)
        if left.isdigit():
            self.num, self.column = int(left), right
        else:
            self.num, self.column = int(right), left

        context.add('column'+str(self.column), self.column)
        context.add('addnum'+str(self.num), self.num)

        var_column = VarExpression('column'+str(self.column))
        var_num = VarExpression('addnum'+str(self.num))

        return SelectoneExpression(self.df, var_column).interpret(context) + var_num.interpret(context)


class SelectonemutipleExpression(Expression):

    def __init__(self, df, expr_one):
        Expression.__init__(self)
        self.df = df
        self.expr_one = expr_one

    def interpret(self, context):
        left, right = (self.expr_one.interpret(context).split("*"))
        print(left, right)
        if left.isdigit():
            self.num, self.column = int(left), right
        else:
            self.num, self.column = int(right), left

        context.add('column'+str(self.column), self.column)
        context.add('num'+str(self.num), self.num)

        var_column = VarExpression('column'+str(self.column))
        var_num = VarExpression('num'+str(self.num))

        return SelectoneExpression(self.df, var_column).interpret(context) * var_num.interpret(context)


class SelectaddanotherExpression(Expression):

    def __init__(self, df, basedf, expr_another):
        Expression.__init__(self)
        self.df = df
        self.basedf = basedf
        self.expr_another = expr_another
        self.SelectoneExpression = SelectoneExpression(df, expr_another)

    def interpret(self, context):
        basedataframe = self.basedf.interpret(context)
        return pd.concat([basedataframe, self.SelectoneExpression.interpret(context)], axis=1)
