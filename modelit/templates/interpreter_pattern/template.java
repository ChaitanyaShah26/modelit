interface Expression {
    boolean interpret(String context);
}

class ContextCheckExpression implements Expression {
    private String data;
    public ContextCheckExpression(String data) { this.data = data; }

    public boolean interpret(String context) {
        return context.contains(data);
    }
}

class AndExpression implements Expression {
    private Expression expr1, expr2;
    public AndExpression(Expression expr1, Expression expr2) {
        this.expr1 = expr1; this.expr2 = expr2;
    }
    public boolean interpret(String context) {
        return expr1.interpret(context) && expr2.interpret(context);
    }
}

public class InterpreterDemo {
    public static void main(String[] args) {
        Expression isPremium = new ContextCheckExpression("Premium");
        Expression buyingTech = new ContextCheckExpression("Electronics");
        Expression discountRule = new AndExpression(isPremium, buyingTech);

        String currentTransaction = "User is Premium, buying Electronics";
        String otherTransaction = "User is Standard, buying Electronics";

        System.out.println("Transaction 1 gets discount? " + discountRule.interpret(currentTransaction));
        System.out.println("Transaction 2 gets discount? " + discountRule.interpret(otherTransaction));
    }
}