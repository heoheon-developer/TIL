package com.example.fastcampus.hamburger;

public class OriginalBurger implements Hamburger {
	private int price = 1000;
	private String ingredient = "Ham";
	@Override
	public int getPrice() {
		// TODO Auto-generated method stub
		return this.price;
	}
	@Override
	public void prepareIngredient() {
		// TODO Auto-generated method stub
		System.out.println(ingredient + "를 준비합니다");
	}





}
