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
#define BUFSIZE 65536

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
            exit(1);
        }

        char *uri = strtok(NULL, "/");
        uri = strtok(NULL, "/");
        printf("domain: %s\n", uri);

        if ((hostp = gethostbyname(uri)) == 0)
        {
            fprintf(stderr, "%s: unknown host\n", uri);
            exit(1);
        }

        memset(&server, 0, sizeof(server));
        server.sin_family = AF_INET;
        memcpy(&server.sin_addr, hostp->h_addr_list[0], hostp->h_length);
        // server.sin_port = htons(80);

        if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0)
        {
            close(sock);
            fprintf(stderr, "Can't connect to server %s", uri);
            PROMPT();
            continue;
        }

        if (write(sock, buf, strlen(buf)) < 0)
        {
            perror("write");
            exit(1);
        }

        bytesread = read(sock, buf, sizeof(buf));
        buf[bytesread] = '\0';
        fprintf(stdout, "Total Size %d bytes\n", bytesread);
    }
}