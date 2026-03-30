#include <stdio.h>
#include <string.h>

void fera_vibe_os_boot(void) {
    printf("  _____ _____ ____      _       __     ___ ____  _____        ___  ____  \n");
    printf(" |  ___| ____|  _ \\    / \\      \\ \\   / / |  _ \\| ____|      / _ \\/ ___| \n");
    printf(" | |_  |  _| | |_) |  / _ \\      \\ \\ / /| | |_) |  _|      | | | \\___ \\ \n");
    printf(" |  _| | |___|  _ <  / ___ \\      \\ V / | |  _ <| |___     | |_| |___) |\n");
    printf(" |_|   |_____|_| \\_\\/_/   \\_\\      \\_/  |_|_| \\_\\_____|     \\___/|____/ \n");
    printf("\n");
    printf("  Welcome to Fera Vibe OS - the vibe is immaculate\n");
    printf("  Version 0.1.0 | vibe-coded from scratch\n");
    printf("\n");
}

void fera_vibe_os_shell(void) {
    /* Maximum input length including null terminator */
    char input[256];

    printf("[fera-vibe-os]$ ");
    while (fgets(input, sizeof(input), stdin)) {
        /* Strip trailing newline */
        input[strcspn(input, "\n")] = '\0';

        if (strlen(input) == 0) {
            /* empty line */
        } else if (strcmp(input, "help") == 0) {
            printf("  Available commands:\n");
            printf("    help   - show this help message\n");
            printf("    vibe   - check the vibe level\n");
            printf("    uname  - print OS info\n");
            printf("    exit   - shut down Fera Vibe OS\n");
        } else if (strcmp(input, "vibe") == 0) {
            printf("  Vibe level: IMMACULATE ✨\n");
        } else if (strcmp(input, "uname") == 0) {
            printf("  Fera Vibe OS 0.1.0 vibe-coded kernel\n");
        } else if (strcmp(input, "exit") == 0) {
            printf("  Shutting down... stay vibing ✌️\n");
            return;
        } else {
            printf("  %s: command not found (type 'help' for commands)\n", input);
        }

        printf("[fera-vibe-os]$ ");
    }
}

int main(void) {
    fera_vibe_os_boot();
    fera_vibe_os_shell();
    return 0;
}
