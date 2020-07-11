package algorithm.java.question;


import java.util.*;

public class test01 {


    public static void main(String[] args){


        test01 test = new test01();

        String[] participant = {"heon", "kim", "choi"};
        String[] completion = {"kim", "choi"};

        String rtn = test.solution(participant, completion);

        System.out.println(rtn);



    }




    public String solution (String[] participant, String[] completion ){

        Arrays.sort(participant);

        Arrays.sort(completion);
        
        
        int i;

        for (i=0;  i < completion.length; i++){

            if (!participant[i].equals(completion[i])){

                return participant[i];
            }


        }





        return null;
    }








    
}