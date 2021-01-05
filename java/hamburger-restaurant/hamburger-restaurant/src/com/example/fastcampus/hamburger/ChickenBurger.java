package com.example.fastcampus.hamburger;

public class ChickenBurger implements Hamburger {
	private int price = 2000;
	private String ingredient = "Chicken";
	@Override
	public int getPrice() {
		// TODO Auto-generated method stub
		return price;
	}
	@Override
	public void prepareIngredient() {
		// TODO Auto-generated method stub
		System.out.println(ingredient + "를 준비합니다");
	}

	//To-do 인터페이스에서 만든 메서드를 재정의하여 구현합니다.
	
	
}
