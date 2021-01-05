package com.example.fastcampus.hamburger;

public class CheeseBurger implements Hamburger {
	private int price = 1500;
	private String ingredient = "Cheese";
	@Override
	public int getPrice() {
		// TODO Auto-generated method stub
		return price;
	}
	@Override
	public void prepareIngredient() {
		System.out.println(ingredient + "를 준비합니다");
		
	}


}
