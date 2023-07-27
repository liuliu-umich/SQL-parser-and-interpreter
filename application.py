class Application():

    # select one column from the dataframe
    @staticmethod
    def selectone(df, one):
        # context
        context = Context()
        context.add('df', df)
        context.add('one', one)

        # 构建表达式
        dataframe = VarExpression('df')
        var_one = VarExpression('one')

        # 再构建变量来进行计算，看起来啰嗦，但这样构建多种不同表达式计算就变得简单
        result = SelectoneExpression(dataframe, var_one)
        return result.interpret(context)

    # select one column from the dataframe and multiple a number
    # @staticmethod
    # def selectonemutiple(df, one):
    #     left, right = (one.split("*"))
    #     if left.isdigit():
    #         num, column = int(left), right
    #     else:
    #         num, column = int(right), left

    #     # context
    #     context = Context()
    #     context.add('df', df)
    #     context.add('num', num)
    #     context.add('column', column)

    #     # 构建表达式
    #     dataframe = VarExpression('df')
    #     var_num = VarExpression('num')
    #     var_column = VarExpression('column')

    #     # 再构建变量来进行计算，看起来啰嗦，但这样构建多种不同表达式计算就变得简单
    #     result = SelectonemutipleExpression(dataframe, var_column, var_num)
    #     return result.interpret(context)

    @staticmethod
    def selectmore(df, *columns):
        if (len(columns) < 1):
            return print("error, need a column name")

        if (len(columns) == 1):
            return Application.selectone(df, columns[0])

        context = Context()
        # 构建执行环境
        for i, column in enumerate(columns):
            context.add('column' + str(i), column)

        context.add('df', df)

        # get basedataframe data
        basedataframe = Application.selectone(df, columns[0])
        context.add('basedataframe', basedataframe)

        # 构建表达式
        dataframe = VarExpression('df')
        baseframe = VarExpression('basedataframe')

        # 如果数量超过1个则累加表达式再求值
        for i in range(1, len(columns)):
            next_expression = VarExpression('column' + str(i))
            # 表达式不断累加
            expression = SelectaddanotherExpression(
                dataframe, baseframe, next_expression)
            basedataframe = expression.interpret(context)
            context.add('basedataframe', basedataframe)

        return basedataframe

    @staticmethod
    def fromfile(filename):
        pass

    @staticmethod
    def wherefilter(df, condition):
        pass

    @staticmethod
    def groupby(df, column):
        pass

    @staticmethod
    def having(df, condition):
        pass

    @staticmethod
    def orderby(df, column):
        pass

    @staticmethod
    def createtable(name, column):
        pass

    @staticmethod
    def deletetable(name, column):
        pass

    @staticmethod
    def inserttable(name, column):
        pass
