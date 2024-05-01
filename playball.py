from textx import metamodel_from_file
PlayBall_mm = metamodel_from_file('PlayBall.tx')
PlayBall_model = PlayBall_mm.model_from_file('fizzbuzz.playball')

#a dictionary to store the programs state (variables and their values)
state = dict()

class PlayBall:

    """
    Retrieves the value of given variable from the program's state.
    targertVar - given variable whose value is retrieved from the state.
    state - the current state of the program. a dictionary of all variables and their values.
    """
    def varmap(self, targetVar, state):
        #checks if targetVar is in the state and returns its value
        if targetVar in state:
            return state[targetVar]
        #raises an error if targetVar is not in the state
        else:
            raise ValueError("Error: Var not found " + targetVar)
    
    """
    Executes a for loop in the style of python range loop from expr1 to expr2.
    expr1 - variable or int value that is start of the range loop.
    expr2 - variable or int value that is the end of the range loop.
    statements - the code in the loop (body) to be executed.
    """
    def loopInterpreter(self, expr1, expr2, statements):
        #retrieve values of expr1/expr2 from state if not ints
        if(expr1 in state):
            expr1 = self.varmap(expr1, state)
        if(expr2 in state):
            expr2 = self.varmap(expr2, state)
        #perform the looping function and execute the loop code
        for i in range(expr1, expr2):
            self.interpret(statements)

    """
    Computes math operations with the given operator and operands.
    operator - the math operator.
    var - the variable where the result is stored after computation.
    expr1 - the left side operand.
    expr2 - the right side operand.
    """
    def mathComputer(self, operator, var, expr1, expr2):
        #retrieve values of expr1/expr2 from state if not ints
        if(expr1 in state):
            expr1 = self.varmap(expr1, state)
        if(expr2 in state):
            expr2 = self.varmap(expr2, state)
        #matches the operator with correct one and computes and stores result in the state
        match operator:
            case "+":
                state[var] =  expr1 + expr2
            case "-":
                state[var] = expr1 - expr2
            case "/":
                state[var] = expr1 / expr2
            case "*":
                state[var] = expr1 * expr2
            case "%":
                state[var] = expr1 % expr2           
            case "^":
                state[var] = expr1 ** expr2
    
    """
    Parses if statements with given equality operator and operands.
    eqoperator - the equality operator.
    expr1 - the left side operand.
    expr2 - the right side operand.
    statements - - the code in the if statement (body) to be executed.
    """
    def ifParser(self, eqoperator, expr1, expr2, statements):
        #retrieve values of expr1/expr2 from state if not boolean
        if(expr1 in state):
            expr1 = self.varmap(expr1, state)
        if(expr2 in state):
            expr2 = self.varmap(expr2, state)
        #matches the equality operator with correct one performs the operation and executes body code if needed
        match eqoperator:
            case "==":
                if(expr1 == expr2):
                    self.interpret(statements)
            case "<":
                if(expr1 < expr2):
                    self.interpret(statements)
            case "<=":
                if(expr1 <= expr2):
                    self.interpret(statements)
            case ">":
                if(expr1 > expr2):
                    self.interpret(statements)
            case ">=":
                if(expr1 >= expr2):
                    self.interpret(statements)         
            case "!=":
                if(expr1 != expr2):
                    self.interpret(statements)   
   
    """
    interprets the program with the help of textx which creates a model of the language from the given grammar
    """
    def interpret(self, model):
        #goes through each statement and matches the statement with their correct type and executes the code
        for statement in model.statements:
            if statement.__class__.__name__ == "AssignmentStatement":
                state[statement.var] = statement.expr
            if statement.__class__.__name__ == "PrintStatement":
                if(statement.expr in state):
                    print(state[statement.expr])
                else:
                    print(statement.expr)
            if statement.__class__.__name__ == "DeleteStatement":
                del state[statement.var]
            if statement.__class__.__name__ == "LoopStatement":
                self.loopInterpreter(statement.expr1, statement.expr2, statement)
            if statement.__class__.__name__ == "MathStatement":
                self.mathComputer(statement.operator, statement.var1, statement.expr1, statement.expr2)
            if statement.__class__.__name__ == "IfStatement":
                self.ifParser(statement.eqoperator, statement.expr1, statement.expr2, statement)
            #Negate if statements are ones where the opposite is true
            #In PlayBall OUT or False are both False. SAFE and True are both True
            #ex) if not FALSE, if !OUT
            if statement.__class__.__name__ == "NegateIfStatement":
                if (statement.expr1 == False or statement.expr1 == "OUT"):
                    self.interpret(statement)
            #examples of valide IfStatements) if True, if SAFE
            if statement.__class__.__name__ == "ValidateIfStatement":
                if (statement.expr1 == True or statement.expr1 == "SAFE"):
                    self.interpret(statement)


#Interprets the given playball program with the help of textx
playball = PlayBall()
playball.interpret(PlayBall_model)