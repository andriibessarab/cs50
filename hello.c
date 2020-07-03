#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Asking user for his name
    string name = get_string("What's your name?\n");
    
    //Say hello to the user
    printf("hello, %s\n", name);
}