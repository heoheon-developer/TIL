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
	// FAMILY 등급과 VIP 등급의 세일즈 전략을 2가지로 결정합니다.
	
	public SalesPriceReport(List<Member> list) {
		
		
	}
	
	public void generateSaleReport(int price) {
		
		// To-do 모든 FAMILY 등급의 회원과, VIP 등급의 회원의 세일즈 보고서를 만듭니다.
		
		int salePrice = 0;
		// FAMILY 등급
		
		System.out.println("등급과 가격에 따른 세일 비율은 " + ratio + "이며, 가격은 " + salePrice + "입니다."); 
	
	
		//VIP 등급
		System.out.println("등급과 가격에 따른 세일 비율은 " + ratio + "이며, 가격은 " + salePrice + "입니다.");
				
		
		System.out.println("==========================================================");
		System.out.println();
	
	}
}
