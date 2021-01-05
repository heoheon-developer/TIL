package com.example.fastcampus.machin;

import java.util.ArrayList;
import java.util.List;

import com.example.fastcampus.hamburger.Hamburger;

public class HamburgerOrderMachine {
	private List<Hamburger> hamburgerList;

	public HamburgerOrderMachine() {
		// TODO 여기서 hamburgerList 를 초기화 합니다.	
		this.hamburgerList = new ArrayList<>();
}

	public void order(Hamburger hamburger) {
		// TODO 주문 받은 햄버거를 hamburgerList에 저장합니다.
		
		this.hamburgerList.add(hamburger);		
		
	}

	public int completeOrder() {
		int totalPrice = 0;

		// TODO 여기서 hamburgerList를 순회하며
		//  1)각 햄버거들의 재료를 출력하고
		//  2)동시에 각 가격을 조회하여 합산한 총 가격을 구한 후 return 합니다.
		
		for(Hamburger item :  this.hamburgerList) {
			
			totalPrice += item.getPrice();
			item.prepareIngredient();
			
			
		}
		
		
		return totalPrice;
	}

}
