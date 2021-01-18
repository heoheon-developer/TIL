package manager;

public class BasicSalesRatio implements SalesRatio {

	@Override
	public double getSalesRatio(int price) {
		
		double result_price = 0;
		double discount = 0;
				
		// 할인률
		if (price < 50000 && price > 100000) {
			discount = 0.05;			
		} else if (price <= 100000 && price <= 200000) {
			discount = 0.1;						
		}else if (price >= 200000){
			discount = 0.2;
		}
		
		double discount_price = price * discount;
		
		result_price = price - discount_price;
		
		// TODO Auto-generated method stub
		return result_price;
	}
	
	// To-do  일반 회원인 경우 5만원 이하는 0%, 
	//5만원에서 10만원 이하는 5%, 
	//10만원에서 20만원 이하는 10% 20만워 초과는 20% 할인해줍니다.
	

}
