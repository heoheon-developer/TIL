package report;

import java.util.List;

import manager.BasicSalesRatio;
import manager.SalesRatio;
import manager.VIPSalesRatio;
import member.Member;

public class SalesPriceReport {

	List<Member> list;
	
	double ratio = 0.0;
	SalesRatio salesStrategy[] = {,};
	// FAMILY ��ް� VIP ����� ������ ������ 2������ �����մϴ�.
	
	public SalesPriceReport(List<Member> list) {		
		for (Member member : list) {
			
			
		}
		
		
	}
	
	public void generateSaleReport(int price) {
		
		// To-do ��� FAMILY ����� ȸ����, VIP ����� ȸ���� ������ ������ ����ϴ�.
		
		BasicSalesRatio basicSalesRatio = new BasicSalesRatio();
		double result_price_family = basicSalesRatio.getSalesRatio(price);
		
		int salePriceFamily = (int) Math.round(result_price_family);
		// FAMILY ���		
		System.out.println("��ް� ���ݿ� ���� ���� ������ " + ratio + "�̸�, ������ " + salePriceFamily + "�Դϴ�."); 
	
		VIPSalesRatio vipSalesRatio = new VIPSalesRatio();
		
		double result_price_vip = vipSalesRatio.getSalesRatio(price);
		
		int salePrice_vip = (int) Math.round(result_price_vip);		
	
		//VIP ���
		System.out.println("��ް� ���ݿ� ���� ���� ������ " + ratio + "�̸�, ������ " + salePrice_vip + "�Դϴ�.");
				
		
		System.out.println("==========================================================");
		System.out.println();
	
	}
}
