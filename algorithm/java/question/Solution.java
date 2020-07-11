package algorithm.java.question;

import java.util.*;
class Solution {

    public static void main(final String[] args){


        String rtn = "";

        final Solution sol = new Solution();

        final String[] participant = {"kim","lee","choi"};
        final String[] completion = {"kim", "lee"};


        rtn = sol.solution(participant, completion);


        System.out.println(rtn);



    }

    public String solution(final String[] participant, final String[] completion) {
            
        
        Map<String, Integer> hash = new HashMap<>();



        for (String item : participant){

            hash.put(item, hash.getOrDefault(item,0) + 1);

        }


        for (String item : completion){


            hash.put(item, hash.get(item)  - 1);
        }


        for (String key : hash.keySet()){
            if (hash.get(key) !=0){

                return key;

            }
        }

        return null;

    }
}
