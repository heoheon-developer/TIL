package com.example.fastcampus.hamburger;

public class BulgogiBurger implements Hamburger {
	private int price = 2000;
	private String ingredient = "Bulgogi";
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
