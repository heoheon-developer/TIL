public class PhoneBook {





    public static void main(String[] args){




        PhoneBook pb = new PhoneBook();


        String[] phone_book = {"119", "97674223", "1195524421"};

        boolean rtn = pb.solution(phone_book);

        System.out.println(rtn);






    }



    public boolean solution(String[] phone_book){

        boolean rtn = true;


        for(int i = 0; i < phone_book.length-1; i++){

            System.out.println(i);

            for (int j = i + 1; j<phone_book.length; j++){

                System.out.println(j);
                

                if(phone_book[i].startsWith(phone_book[j])){return false;}
                if(phone_book[j].startsWith(phone_book[i])){return false;}


            }
        }
        return rtn;
    }
    
}