//1부터n까지의 합


import java.util.*;

public class Hab{

   public static void main(String[] args){



        Scanner stdIn = new Scanner(System.in);

        
        System.out.print("정수 n을 입력하세요");
        int n = stdIn.nextInt();

        int sum=0;

        for (int i = 0; i <=n; i++){


            sum +=i;
        }

        System.out.println("1부터 " + n + "까지의 합은 "+ sum+ "입니다");
        stdIn.close();

    }








}


