public class Answer {   
    public static int answer(String s) { 

        // Your code goes here.
        int count = 0;
        int count_right = 0;
        
        for(int i = 0; i < s.length(); i++)
        {
            char c = s.charAt(i);
            
            if( c == '-')
            {
                continue;
            }
            
            if( c == '>')
            {
                count_right++;
            }
            
            if( c == '<' )
            {
                count += count_right;
            }
        }
        
        return 2*count;
    } 

    public static void main(String[] args)
    {
        Answer a = new Answer();
        System.out.println(a.answer("---<->>->>--<-"));
    }
}