package manager;

public class VIPSalesRatio implements SalesRatio {

	@Override
	public double getSalesRatio(int price) {
		double result_price = 0;
		double discount = 0;
				
		// ���η�
		if (price < 50000 && price < 100000) {
			discount = 0.05;			
		} else if (price <= 100000 && price <= 200000) {
			discount = 0.2;						
		}else if (price >= 200000){
			discount = 0.3;
		}
		
		double discount_price = price * discount;
		
		result_price = price - discount_price;
		
		// TODO Auto-generated method stub
		return result_price;
	}
	
	
	
	//To-do VIP ȸ���� ��� 5���� ���ϴ� 0%, 
	//5�������� 10���� ���ϴ� 10%, 10�������� 20���� ���ϴ� 20%, 
	//20���� �̻��� 30%�� ������ �ݴϴ�. 
	
}


