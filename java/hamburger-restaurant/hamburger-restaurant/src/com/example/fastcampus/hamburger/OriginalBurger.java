package com.example.fastcampus.hamburger;

public class OriginalBurger implements Hamburger {
	private int price = 1000;
	private String ingredient = "Ham";
	@Override
	public void printTotalPrice() {
		// TODO Auto-generated method stub
		System.out.println("오리지날 버거의 가격은"+this.price+"입니다");
		
	}
	@Override
	public void printIngredient() {
		// TODO Auto-generated method stub
		System.out.println("오리지날 버거의 재료는"+this.ingredient+"입니다");
	}
	
	//To-do 인터페이스에서 만든 메서드를 재정의하여 구현합니다.




}
