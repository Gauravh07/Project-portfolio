/*
 * client.c
 */

// Divyesh Biswas 33623665
// Gaurav Hareesh 33576520
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "csapp.h"

int main(int argc, char **argv) 
{
    int clientfd;
    char *num1, *num2;
    char *host, *port;

    if (argc != 3) {
        fprintf(stderr, "usage: %s <num1> <num2>\n", argv[0]);
        exit(0);
    }

    num1 = argv[1];
    num2 = argv[2];

    host = "localhost";
    port = "8080";

    clientfd = Open_clientfd(host, port);

    // Safely allocate buffers with clear initialization
    char body[MAXLINE] = {0};
    char header[MAXLINE] = {0};
    char values[MAXLINE] = {0};

    // Build the body using snprintf for safer string handling
    snprintf(body, sizeof(body), 
        "<?xml version=\"1.0\"?>\r\n"
        "<methodCall>\r\n"
        "<methodName>sample.addmultiply</methodName>\r\n"
        "<params>\r\n"
        "<param><value><double>%s</double></value></param>\r\n"
        "<param><value><double>%s</double></value></param>\r\n"
        "</params>\r\n"
        "</methodCall>\r\n", 
        num1, num2);

    // Build HTTP POST Header using snprintf
    snprintf(header, sizeof(header), 
        "POST /RPC2 HTTP/1.1\r\n"
        "Content-Type:text/xml\r\n"
        "User-Agent:XML-RPC.NET\r\n"
        "Content-Length:%ld\r\n"
        "Expect:100-continue\r\n"
        "Connection:Keep-Alive\r\n"
        "Host:localhost:8080\r\n"
        "\r\n"
        "%s", 
        (long)strlen(body), body);

    // Send the request
    Rio_writen(clientfd, header, strlen(header));

    // Read the response body
    rio_t rio;
    Rio_readinitb(&rio, clientfd);

    char response_line[MAXLINE];
    int values_index = 0;

    // Search for all values in <double> tags in the response
    while (Rio_readlineb(&rio, response_line, MAXLINE) != 0)
    {
        char *start = strstr(response_line, "<double>");
        if (start != NULL)
        {
            start += strlen("<double>");
            char *end = strstr(start, "</double>");
            if (end != NULL)
            {
                // Safely copy the value
                char value[MAXLINE];
                size_t value_len = end - start;
                strncpy(value, start, value_len);
                value[value_len] = '\0';

                // Append to values with a space, being careful not to overflow
                if (values_index > 0) {
                    if (values_index < sizeof(values) - 1) {
                        values[values_index++] = ' ';
                    }
                }

                // Safely append the value to the values string
                size_t remaining = sizeof(values) - values_index;
                strncat(values + values_index, value, remaining - 1);
                values_index += strlen(value);
            }
        }
    }

    // Print values
    printf("%s\n", values);
    
    Close(clientfd);
    exit(0);
}