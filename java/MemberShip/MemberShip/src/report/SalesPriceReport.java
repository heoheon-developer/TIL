package report;

import java.util.List;

import manager.BasicSalesRatio;
import manager.SalesRatio;
import manager.VIPSalesRatio;
import member.Member;

public class SalesPriceReport {

	List<Member> list;
	
	double ratio = 0.0;
	SalesRatio salesStrategy[] = { , };
	// FAMILY ��ް� VIP ����� ������ ������ 2������ �����մϴ�.
	
	public SalesPriceReport(List<Member> list) {
		
		
	}
	
	public void generateSaleReport(int price) {
		
		// To-do ��� FAMILY ����� ȸ����, VIP ����� ȸ���� ������ ������ ����ϴ�.
		
		int salePrice = 0;
		// FAMILY ���
		
		System.out.println("��ް� ���ݿ� ���� ���� ������ " + ratio + "�̸�, ������ " + salePrice + "�Դϴ�."); 
	
	
		//VIP ���
		System.out.println("��ް� ���ݿ� ���� ���� ������ " + ratio + "�̸�, ������ " + salePrice + "�Դϴ�.");
				
		
		System.out.println("==========================================================");
		System.out.println();
	
	}
}
