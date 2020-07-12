public class Cal{

    public static void main(String[] args){

    
  
     Cal cal = new Cal();

     String rtn = cal.solution(5, 24);
    
     System.out.println(rtn);
    




    }



    public String solution(int a, int b){

        int total = 0;
        String w[] = {"FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"};
        int m[] = {31, 29, 31, 30, 31, 30,31, 31, 30, 31, 30, 31};
        for(int i =0;i<a-1;i++){
            total += m[i];
        }
        total += b-1;
        String answer = w[total%7];
        return answer;


    }



}