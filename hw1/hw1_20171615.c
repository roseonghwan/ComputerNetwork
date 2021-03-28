// Student ID : 20171615
// Name : Seonghwan Noh

#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define GETCMD "get"
#define QUITCMD "quit"
#define BUFSIZE 0x10000

static inline void PROMPT()
{
    printf("\n> ");
    fflush(stdout);
}

int main()
{
    int sock,
        bytesread,
        socktoserver = -1;
    char buf[BUFSIZE],
        fname[BUFSIZE];
    struct hostent *hostp;
    struct sockaddr_in server;

    printf("Student ID : 20171615\n");
    printf("Name : Seonghwan Noh\n");

    PROMPT();

    while (true)
    {
        if (!fgets(buf, BUFSIZE - 1, stdin))
        {
            if (ferror(stdin))
            {
                perror("stdin");
                exit(1);
            }
            exit(0);
        }

        char *cmd = strtok(buf, " \t\n\r");

        if ((cmd == NULL) || (strcmp(cmd, "") == 0))
        {
            PROMPT();
            continue;
        }
        else if (strcasecmp(cmd, QUITCMD) == 0)
        {
            exit(0);
        }

        if (!strcasecmp(cmd, GETCMD) == 0)
        {
            printf("Wrong command %s\n", cmd);
            PROMPT();
            continue;
        }

        // connect to a server

        // NEED TO IMPLEMENT HERE

        if ((sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
        {
            perror("socket");
            PROMPT();
            continue;
        }

        cmd = strtok(NULL, " \t\r\n");
        cmd = strtok(cmd, "/");
        cmd = strtok(NULL, "/");

        char domain[strlen(cmd)];
        strcpy(domain, cmd);

        cmd = strtok(NULL, "/");
        char path[strlen(cmd)];
        strcpy(path, cmd);

        cmd = strtok(NULL, "/");
        char fileName[strlen(cmd)];
        strcpy(fileName, cmd);

        if ((hostp = gethostbyname(domain)) == 0)
        {
            fprintf(stderr, "%s: unknown host\n", domain);
            PROMPT();
            continue;
        }

        char *ip = inet_ntoa(*(struct in_addr *)hostp->h_addr_list[0]);

        memset(&server, 0, sizeof(server));
        server.sin_family = AF_INET;
        server.sin_addr.s_addr = inet_addr(ip);
        server.sin_port = htons(80);

        if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0)
        {
            close(sock);
            fprintf(stderr, "Can't connect to server %s", domain);
            PROMPT();
            continue;
        }
        char send_msg[BUFSIZE];
        sprintf(send_msg, "GET /%s/%s HTTP/1.0\r\nHost: %s\r\nUser-agent: HW1/1.0 Connection: close\r\n\r\n", path, fileName, domain);
        printf("%s\n", send_msg);

        if (write(sock, send_msg, strlen(send_msg)) < 0)
        {
            perror("write");
            PROMPT();
            continue;
        }

        char response_msg[BUFSIZE];

        if ((bytesread = recv(sock, response_msg, sizeof response_msg, 0)) < 0)
        {
            printf("Failed read()\n");
            PROMPT();
            continue;
        }

        response_msg[bytesread] = '\0';
        printf("Total Size %d bytes\n", bytesread);
        printf("%s\n", response_msg);

        close(sock);
        PROMPT();
    }
}