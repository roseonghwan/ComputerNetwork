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
#define BUFSIZE 1024

static inline void PROMPT()
{
    printf("\n> ");
    fflush(stdout);
}

int main()
{
    int sock, bytesread, socktoserver = -1;
    char buf[BUFSIZ], fname[BUFSIZ];
    struct hostent *hostp;
    struct sockaddr_in server;

    printf("Student ID : 20171615\n");
    printf("Name : Seonghwan Noh\n");

    PROMPT();

    for (;;)
    {
        if (!fgets(buf, BUFSIZ - 1, stdin))
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
        char sep[strlen(cmd)];
        strcpy(sep, cmd);

        char domain[strlen(cmd)];

        char fileName[strlen(cmd)];

        cmd = strtok(NULL, " \t\n\r");
        // printf("cmd: %s\n", cmd);
        char full_path[BUFSIZE];
        strcpy(full_path, cmd);
        // printf("full_path: %s\n", full_path);

        char path[BUFSIZE];
        strcpy(path, full_path);
        char *image_path = strtok(path, "/");

        // not http
        if (strcmp(image_path, "http:") != 0)
        {
            printf("Only support http, not https\n");
            PROMPT();
            continue;
        }

        image_path = strtok(NULL, "/");
        image_path = strtok(NULL, " \t\n\r");
        // printf("path2: %s\n", image_path);

        // find picture name
        char *tmp = strtok(full_path, "/");
        while (tmp != NULL)
        {
            strcpy(fname, tmp);
            tmp = strtok(NULL, "/");
        }

        // find domain name
        cmd = strtok(cmd, "/");
        cmd = strtok(NULL, "/");
        strcpy(domain, cmd);
        // printf("domain: %s\n", domain);

        // find port number
        tmp = strtok(domain, ":");
        strcpy(domain, tmp);

        tmp = strtok(NULL, ":");
        // printf("port: %s\n", tmp);

        char *port = "80";
        bool alloced = false;
        // if url has portNum
        if (tmp != NULL)
        {
            port = malloc(strlen(tmp));
            strcpy(port, tmp);
            alloced = true;
        }
        if (alloced == true)
            free(port);

        if ((hostp = gethostbyname(domain)) == 0)
        {
            fprintf(stderr, "%s: unknown host\n", domain);
            printf("cannot connect to server %s %s\n", domain, port);
            PROMPT();
            continue;
        }

        char *ip = inet_ntoa(*(struct in_addr *)hostp->h_addr_list[0]);
        // printf("ip: %s\n", ip);

        memset(&server, 0, sizeof(server));
        server.sin_family = AF_INET;
        server.sin_addr.s_addr = inet_addr(ip);
        memcpy((void *)&server.sin_addr, hostp->h_addr_list[0], hostp->h_length);
        server.sin_port = htons(80);

        if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0)
        {
            close(sock);
            fprintf(stderr, "Can't connect to server %s", domain);
            PROMPT();
            continue;
        }
        char send_msg[BUFSIZE];
        sprintf(send_msg, "GET /%s HTTP/1.0\r\nHost: %s\r\nUser-agent: HW1/1.0\r\nConnection: close\r\n\r\n", image_path, domain);
        printf("%s\n", send_msg);

        if (write(sock, send_msg, strlen(send_msg)) < 0)
        {
            perror("write");
            PROMPT();
            continue;
        }

        char response_msg[BUFSIZE];
        // receive HTTP response message
        if ((bytesread = recv(sock, response_msg, sizeof response_msg, 0)) < 0)
        {
            printf("Failed read()\n");
            PROMPT();
            continue;
        }

        response_msg[bytesread] = '\0';

        char *status = malloc(3);
        strncpy(status, response_msg + 9, 3);
        // printf("status: %s\n", status);
        int status_code = atoi(status);
        int start_response = strlen(response_msg);
        // printf("status_code: %d, start_response: %d\n", status_code, start_response);

        switch (status_code)
        {
        case 200:
            break;
        case 301:
            printf("%d Moved Permanently\n", status_code);
            PROMPT();
            continue;
            break;
        case 400:
            printf("%d Bad request\n", status_code);
            PROMPT();
            continue;
            break;
        case 404:
            printf("%d Not Found\n", status_code);
            PROMPT();
            continue;
            break;
        case 505:
            printf("%d HTTP Version Not Supported\n", status_code);
            PROMPT();
            continue;
            break;
        }
        free(status);

        // get content size
        char *filesize = strtok(response_msg, "\n");

        while (filesize != NULL)
        {
            filesize = strtok(NULL, ":");
            if (strcmp(filesize, "Content-Length") == 0)
            {
                filesize = strtok(NULL, "\n");
                break;
            }
            filesize = strtok(NULL, "\n");
        }
        int total_size = atoi(filesize);
        printf("Total Size %d bytes\n", total_size);

        char *body_data = strtok(NULL, "\n");
        // printf("receive_data: %s\n", receive_data);

        // seperate header
        while (body_data[0] != '\r')
        {
            body_data = strtok(NULL, "\n");
        }
        body_data = strtok(NULL, "\n");

        FILE *fp = fopen(fname, "wb");

        int start_body = strlen(body_data);

        // Don't write if HTTP response header has no data
        if (*body_data != 0)
        {
            // seperate header size
            fwrite(body_data, bytesread - (start_response - start_body), 1, fp);
        }
        int i = 1, download = 0;
        while (true)
        {
            // Receive data left in socket
            memset(response_msg, 0, sizeof response_msg);
            int recv_data_size = recv(sock, response_msg, sizeof response_msg, 0);
            response_msg[recv_data_size] = '\0';

            // Complete download if downloaded file size is same or bigger than content length
            if (download >= total_size)
            {
                printf("Download Complete: %s, %d/%d\n", fname, download, total_size);
                break;
            }

            // Write received data from socket
            fwrite(response_msg, recv_data_size, 1, fp);

            // Check current download size
            download = ftell(fp);

            if (download >= (total_size / 10) * i)
            {
                printf("Current Downloading %d/%d (bytes) %d%%\n", download, total_size, (int)(download * 100 / total_size));
                i++;
            }
        }

        fclose(fp);
        close(sock);
        PROMPT();
    }
}