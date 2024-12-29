/* 
 * tsh - A tiny shell program with job control
 * 
 * Divyesh Biswas 33623665
 * Gaurav Hareesh 33576520
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>

pid_t fg_pid = 0; 

/* Misc manifest constants */
#define MAXLINE    1024   /* max line size */
#define MAXARGS     128   /* max args on a command line */
#define MAXJOBS      16   /* max jobs at any point in time */
#define MAXJID    1<<16   /* max job ID */

/* Job states */
#define UNDEF 0 /* undefined */
#define FG 1    /* running in foreground */
#define BG 2    /* running in background */
#define ST 3    /* stopped */



/* 
 * Jobs states: FG (foreground), BG (background), ST (stopped)
 * Job state transitions and enabling actions:
 *     FG -> ST  : ctrl-z
 *     ST -> FG  : fg command
 *     ST -> BG  : bg command
 *     BG -> FG  : fg command
 * At most 1 job can be in the FG state.
 */

/* Global variables */
extern char **environ;      /* defined in libc */
char prompt[] = "tsh> ";    /* command line prompt (DO NOT CHANGE) */
int verbose = 0;            /* if true, print additional output */
int nextjid = 1;            /* next job ID to allocate */
char sbuf[MAXLINE];         /* for composing sprintf messages */

struct job_t {              /* The job struct */
    pid_t pid;              /* job PID */
    int jid;                /* job ID [1, 2, ...] */
    int state;              /* UNDEF, BG, FG, or ST */
    char cmdline[MAXLINE];  /* command line */
};
struct job_t jobs[MAXJOBS]; /* The job list */
/* End global variables */


/* Function prototypes */

/* Here are the functions that you will implement */
void eval(char *cmdline);
int builtin_cmd(char **argv);
void do_bgfg(char **argv);
void waitfg(pid_t pid);

void sigchld_handler(int sig);
void sigtstp_handler(int sig);
void sigint_handler(int sig);

/* Here are helper routines that we've provided for you */
int parseline(const char *cmdline, char **argv); 
void sigquit_handler(int sig);

void clearjob(struct job_t *job);
void initjobs(struct job_t *jobs);
int maxjid(struct job_t *jobs); 
int addjob(struct job_t *jobs, pid_t pid, int state, char *cmdline);
int deletejob(struct job_t *jobs, pid_t pid); 
pid_t fgpid(struct job_t *jobs);
struct job_t *getjobpid(struct job_t *jobs, pid_t pid);
struct job_t *getjobjid(struct job_t *jobs, int jid); 
int pid2jid(pid_t pid); 
void listjobs(struct job_t *jobs);

void usage(void);
void unix_error(char *msg);
void app_error(char *msg);
typedef void handler_t(int);
handler_t *Signal(int signum, handler_t *handler);

int handle_redirection(char **argv);
void parse_redirection(char **argv, char **input_file, char **output_file, 
                      char **error_file, char **append_file, char **pipe_cmd);
void setup_pipe(int pipefd[2]);
void close_pipe(int pipefd[2]);

/*
 * main - The shell's main routine 
 */
int main(int argc, char **argv) 
{
    char c;
    char cmdline[MAXLINE];
    int emit_prompt = 1; /* emit prompt (default) */

    /* Redirect stderr to stdout (so that driver will get all output
     * on the pipe connected to stdout) */
    dup2(1, 2);

    /* Parse the command line */
    while ((c = getopt(argc, argv, "hvp")) != EOF) {
        switch (c) {
        case 'h':             /* print help message */
            usage();
	    break;
        case 'v':             /* emit additional diagnostic info */
            verbose = 1;
	    break;
        case 'p':             /* don't print a prompt */
            emit_prompt = 0;  /* handy for automatic testing */
	    break;
	default:
            usage();
	}
    }

    /* Install the signal handlers */

    /* These are the ones you will need to implement */
    Signal(SIGINT,  sigint_handler);   /* ctrl-c */
    Signal(SIGTSTP, sigtstp_handler);  /* ctrl-z */
    Signal(SIGCHLD, sigchld_handler);  /* Terminated or stopped child */
    /* This one provides a clean way to kill the shell */
    Signal(SIGQUIT, sigquit_handler); 

    /* Initialize the job list */
    initjobs(jobs);

    /* Execute the shell's read/eval loop */
    while (1) {
    /* Read command line */
    if (emit_prompt) {
        printf("%s", prompt);
        fflush(stdout);
    }

    if (fgets(cmdline, MAXLINE, stdin) == NULL) {
        if (feof(stdin)) { /* End of file (ctrl-d) */
            printf("\n"); // Print newline for better user experience
            fflush(stdout);
            fflush(stderr);
            exit(0);
        } else if (ferror(stdin)) {
            app_error("fgets error");
        }
    }

    /* Evaluate the command line */
    eval(cmdline);
    fflush(stdout);
    fflush(stdout);
}

    exit(0); /* control never reaches here */
}
  
/* 
 * eval - Evaluate the command line that the user has just typed in
 * herwise,
 * If the user has requested a built-in command (quit, jobs, bg or fg)
 * then execute it immediately. Ot fork a child process and
 * run the job in the context of the child. If the job is running in
 * the foreground, wait for it to terminate and then return.  Note:
 * each child process must have a unique process group ID so that our
 * background children don't receive SIGINT (SIGTSTP) from the kernel
 * when we type ctrl-c (ctrl-z) at the keyboard.  
*/
/* Setup and execute pipeline command */
int setup_pipeline(char **argv, int bg) {
    int pipe_count = 0;
    int pipe_fd[2];
    pid_t first_pid, second_pid;
    char *argv_first[MAXARGS] = {NULL};
    char *argv_second[MAXARGS] = {NULL};
    int first_argc = 0, second_argc = 0;
    
    // Count pipes and split arguments
    for (int i = 0; argv[i] != NULL; i++) {
        if (strcmp(argv[i], "|") == 0) {
            pipe_count++;
            argv[i] = NULL;
            continue;
        }
        
        if (pipe_count == 0) {
            argv_first[first_argc++] = argv[i];
        } else {
            argv_second[second_argc++] = argv[i];
        }
    }
    
    // Prevent multiple pipes
    if (pipe_count > 1) {
        printf("Multiple pipes not supported\n");
        return 0;
    }
    
    if (pipe_count == 0) {
        return 0;  // Not a pipeline
    }
    
    // Create pipe
    if (pipe(pipe_fd) < 0) {
        unix_error("Pipe creation failed");
        return 0;
    }
    
    // Fork first process
    sigset_t mask_one, prev_one;
    sigemptyset(&mask_one);
    sigaddset(&mask_one, SIGCHLD);
    sigprocmask(SIG_BLOCK, &mask_one, &prev_one);
    
    first_pid = fork();
    if (first_pid == 0) {
        // First child process
        setpgid(0, 0);
        
        // Redirect stdout to pipe write end
        close(pipe_fd[0]);
        dup2(pipe_fd[1], STDOUT_FILENO);
        close(pipe_fd[1]);
        
        // Execute first command
        if (execve(argv_first[0], argv_first, environ) < 0) {
            printf("%s: Command not found\n", argv_first[0]);
            exit(0);
        }
    }
    
    // Fork second process
    second_pid = fork();
    if (second_pid == 0) {
        // Second child process
        setpgid(0, 0);
        
        // Redirect stdin to pipe read end
        close(pipe_fd[1]);
        dup2(pipe_fd[0], STDIN_FILENO);
        close(pipe_fd[0]);
        
        // Execute second command
        if (execve(argv_second[0], argv_second, environ) < 0) {
            printf("%s: Command not found\n", argv_second[0]);
            exit(0);
        }
    }
    
    // Parent process
    close(pipe_fd[0]);
    close(pipe_fd[1]);
    
    // Add jobs to job list
    addjob(jobs, first_pid, bg ? BG : FG, argv_first[0]);
    addjob(jobs, second_pid, bg ? BG : FG, argv_second[0]);
    
    if (!bg) {
        signal(SIGTTOU, SIG_IGN);
        tcsetpgrp(STDIN_FILENO, first_pid);
        sigprocmask(SIG_SETMASK, &prev_one, NULL);
        waitfg(first_pid);
        tcsetpgrp(STDIN_FILENO, getpid());
        signal(SIGTTOU, SIG_DFL);
    } else {
        printf("[%d] (%d) %s", pid2jid(first_pid), first_pid, argv_first[0]);
        printf("[%d] (%d) %s", pid2jid(second_pid), second_pid, argv_second[0]);
    }
    
    return 1;  // Pipeline executed
}


int handle_redirection(char **argv) {
    int fd;
    for (int i = 0; argv[i] != NULL; i++) {
        if (strcmp(argv[i], "<") == 0) {
            fd = open(argv[i + 1], 0);  // O_RDONLY is 0
            if (fd < 0) {
                perror("Error opening input file");
                return -1;
            }
            dup2(fd, STDIN_FILENO);
            close(fd);
            argv[i] = NULL; // Remove the redirection operator and filename
        } else if (strcmp(argv[i], ">") == 0) {
            fd = open(argv[i + 1], 1 | 64 | 512, 0700); // O_WRONLY | O_CREAT | O_TRUNC
            if (fd < 0) {
                perror("Error opening output file");
                return -1;
            }
            dup2(fd, STDOUT_FILENO);
            close(fd);
            argv[i] = NULL;
        } else if (strcmp(argv[i], ">>") == 0) {
            fd = open(argv[i + 1], 1 | 64 | 1024, 0700); // O_WRONLY | O_CREAT | O_APPEND
            if (fd < 0) {
                perror("Error opening append file");
                return -1;
            }
            dup2(fd, STDOUT_FILENO);
            close(fd);
            argv[i] = NULL;
        } else if (strcmp(argv[i], "2>") == 0) {
            fd = open(argv[i + 1], 1 | 64 | 512, 0700); // O_WRONLY | O_CREAT | O_TRUNC
            if (fd < 0) {
                perror("Error opening error file");
                return -1;
            }
            dup2(fd, STDERR_FILENO);
            close(fd);
            argv[i] = NULL;
        }
    }
    return 0;  // Return 0 on success
}

void eval(char *cmdline) {
    char *argv[MAXARGS];  // Argument list for execve()
    int bg;               // Background job?
    pid_t pid;

    bg = parseline(cmdline, argv);  // Parse the command line
    if (argv[0] == NULL) {
        return;  // Ignore empty lines
    }

    // Handle built-in commands and pipelines
    if (!builtin_cmd(argv) && !setup_pipeline(argv, bg)) {
        sigset_t mask_one, prev_one;
        sigemptyset(&mask_one);
        sigaddset(&mask_one, SIGCHLD);
        sigprocmask(SIG_BLOCK, &mask_one, &prev_one);   // Block SIGCHLD signals

        if ((pid = fork()) == 0) {  // Child process
            sigprocmask(SIG_SETMASK, &prev_one, NULL);  // Unblock SIGCHLD signals
            setpgid(0, 0);  // New process group

            if (handle_redirection(argv) < 0) {
                // Redirection error, print message and exit child process
                exit(1);
            }

            // Check if command exists and is executable
            if (access(argv[0], X_OK) < 0) {
                printf("%s: Command not found\n", argv[0]);
                exit(1);
            }

            if (execve(argv[0], argv, environ) < 0) {
                printf("%s: Command execution failed\n", argv[0]);
                exit(1);
            }
        }

        // Parent process
        if (!bg) {
            addjob(jobs, pid, FG, cmdline);
            signal(SIGTTOU, SIG_IGN);
            tcsetpgrp(STDIN_FILENO, pid);  // Give terminal control to child
            sigprocmask(SIG_SETMASK, &prev_one, NULL);
            waitfg(pid);
            tcsetpgrp(STDIN_FILENO, getpid());  // Take back terminal control
            signal(SIGTTOU, SIG_DFL);
        } else {
            addjob(jobs, pid, BG, cmdline);
            sigprocmask(SIG_SETMASK, &prev_one, NULL);
            printf("[%d] (%d) %s", pid2jid(pid), pid, cmdline);
        }
    }

    // Make sure all file descriptors are flushed
    fflush(stdout);
    fflush(stderr);
}

/* 
 * parseline - Parse the command line and build the argv array.
 * 
 * Characters enclosed in single quotes are treated as a single
 * argument.  Return true if the user has requested a BG job, false if
 * the user has requested a FG job.  
 */
int parseline(const char *cmdline, char **argv) 
{
    static char array[MAXLINE]; /* holds local copy of command line */
    char *buf = array;          /* ptr that traverses command line */
    char *delim;                /* points to first space delimiter */
    int argc;                   /* number of args */
    int bg;                     /* background job? */

    strcpy(buf, cmdline);
    buf[strlen(buf)-1] = ' ';  /* replace trailing '\n' with space */
    while (*buf && (*buf == ' ')) /* ignore leading spaces */
	buf++;

    /* Build the argv list */
    argc = 0;
    if (*buf == '\'') {
	buf++;
	delim = strchr(buf, '\'');
    }
    else {
	delim = strchr(buf, ' ');
    }

    while (delim) {
	argv[argc++] = buf;
	*delim = '\0';
	buf = delim + 1;
	while (*buf && (*buf == ' ')) /* ignore spaces */
	       buf++;

	if (*buf == '\'') {
	    buf++;
	    delim = strchr(buf, '\'');
	}
	else {
	    delim = strchr(buf, ' ');
	}
    }
    argv[argc] = NULL;
    
    if (argc == 0)  /* ignore blank line */
	return 1;

    /* should the job run in the background? */
    if ((bg = (*argv[argc-1] == '&')) != 0) {
	argv[--argc] = NULL;
    }
    return bg;
}

/* 
 * builtin_cmd - If the user has typed a built-in command then execute
 *    it immediately.  
 */

int builtin_cmd(char **argv) 
{
    if (!strcmp(argv[0], "quit")) { // If the command is quit
        exit(0);
    }
    if (!strcmp(argv[0], "jobs")) { // If the command is jobs
        listjobs(jobs);
        return 1;
    }
    if (!strcmp(argv[0], "bg") || !strcmp(argv[0], "fg")) { // If the command is bg or fg
        do_bgfg(argv);
        return 1;
    }
    return 0;     /* not a builtin command */
}

/* 
 * do_bgfg - Execute the builtin bg and fg commands
 */
void do_bgfg(char **argv) 
{
    struct job_t *jobp = NULL;
    int jid;
    char *id = argv[1];
    
    if (id == NULL) {   // If the argument is not provided
        printf("%s command requires PID or %%jobid argument\n", argv[0]);
        return;
    }

    if (id[0] == '%') { // If the argument is a job id
        jid = atoi(&id[1]);
        jobp = getjobjid(jobs, jid);
        if (jobp == NULL) {
            printf("%s: No such job\n", id);
            return;
        }
    } else if (isdigit(id[0])) {    // If the argument is a process id
        pid_t pid = atoi(id);
        jobp = getjobpid(jobs, pid);
        if (jobp == NULL) {
            printf("(%d): No such process\n", pid);
            return;
        }
    } else {    // If the argument is neither a job id nor a process id
        printf("%s: argument must be a PID or %%jobid\n", argv[0]);
        return;
    }

    if (!strcmp(argv[0], "bg")) {   // If the command is bg
        if (jobp->state == ST) {    // If the job is stopped
            jobp->state = BG;   
            kill(-jobp->pid, SIGCONT);  // Resume the job
            printf("[%d] (%d) %s", jobp->jid, jobp->pid, jobp->cmdline);
        }
    } else if (!strcmp(argv[0], "fg")) {    // If the command is fg
        if (jobp->state == ST || jobp->state == BG) {   
            jobp->state = FG;   // Change the state of the job to foreground
            signal(SIGTTOU, SIG_IGN);
            tcsetpgrp(STDIN_FILENO, jobp->pid);  // Give control of stdin to the child process group
            kill(-jobp->pid, SIGCONT);  // Resume the job
            waitfg(jobp->pid);
            tcsetpgrp(STDIN_FILENO, getpid());  // Return control to the shell
            signal(SIGTTOU, SIG_DFL);
        }
    }
    return;
}

/* 
 * waitfg - Block until process pid is no longer the foreground process
 * The handlers here only apply to foreground processes, whereeas the signal handlers are only called if the 
 * program is sent a signal from outside the foreground
 */

void waitfg(pid_t pid) 
{
    struct job_t *job = getjobpid(jobs, pid);
    while (job != NULL && job->state == FG) {   // Wait until the job is no longer in the foreground
        sleep(1); // Or use a better waiting mechanism if needed
        job = getjobpid(jobs, pid);
    }
}

/*****************
 * Signal handlers
 *****************/

/* 
 * sigchld_handler - The kernel sends a SIGCHLD to the shell whenever
 *     a child job terminates (becomes a zombie), or stops because it
 *     received a SIGSTOP or SIGTSTP signal. The handler reaps all
 *     available zombie children, but doesn't wait for any other
 *     currently running children to terminate.  
 */
void sigchld_handler(int sig) 
{
    int saved_errno = errno;    // Save errno
    pid_t pid;
    int status;

    while ((pid = waitpid(-1, &status, WNOHANG)) > 0) {    // Reap all dead child processes
        deletejob(jobs,pid);       // clear job
    }
    errno = saved_errno;    // Restore errno
}


/* 
 * sigint_handler - The kernel sends a SIGINT to the shell whenver the
 *    user types ctrl-c at the keyboard.  Catch it and send it along
 *    to the foreground job.  
 */

void sigint_handler(int sig) 
{
    pid_t pid = fgpid(jobs);    // Get the pid of the foreground job
    if (pid != 0) {
        int jid = pid2jid(pid);
        printf("Job [%d] (%d) terminated by signal %d\n", jid, pid, sig);
        kill(-pid, SIGINT);        // Send SIGINT to the foreground process group
        struct job_t *job = getjobpid(jobs, pid);        // Remove job from job list and update state
        if (job != NULL) {
            deletejob(jobs, pid);   // Clear the job
        }
    }
}



/*
 * sigtstp_handler - The kernel sends a SIGTSTP to the shell whenever
 *     the user types ctrl-z at the keyboard. Catch it and suspend the
 *     foreground job by sending it a SIGTSTP.  
 */
void sigtstp_handler(int sig) 
{
    pid_t pid = fgpid(jobs);
    if (pid != 0) {    // If there is a foreground job
        int jid = pid2jid(pid); // Get the job id
        printf("Job [%d] (%d) stopped by signal %d\n", jid, pid, sig);
        kill(-pid, SIGTSTP);        // Send SIGTSTP to the foreground job
        struct job_t *job = getjobpid(jobs, pid);        // Update the job state to stopped
        if (job != NULL) {      // If the job exists
            job->state = ST;    // Change the state of the job to stopped
        }
    }
}

/*********************
 * End signal handlers
 *********************/

/***********************************************
 * Helper routines that manipulate the job list
 **********************************************/

/* clearjob - Clear the entries in a job struct */
void clearjob(struct job_t *job) {
    job->pid = 0;
    job->jid = 0;
    job->state = UNDEF;
    job->cmdline[0] = '\0';
}

/* initjobs - Initialize the job list */
void initjobs(struct job_t *jobs) {
    int i;

    for (i = 0; i < MAXJOBS; i++)
	clearjob(&jobs[i]);
}

/* maxjid - Returns largest allocated job ID */
int maxjid(struct job_t *jobs) 
{
    int i, max=0;

    for (i = 0; i < MAXJOBS; i++)
	if (jobs[i].jid > max)
	    max = jobs[i].jid;
    return max;
}

/* addjob - Add a job to the job list */
int addjob(struct job_t *jobs, pid_t pid, int state, char *cmdline) 
{
    int i;
    
    if (pid < 1)
	return 0;

    for (i = 0; i < MAXJOBS; i++) {
	if (jobs[i].pid == 0) {
	    jobs[i].pid = pid;
	    jobs[i].state = state;
	    jobs[i].jid = nextjid++;
	    if (nextjid > MAXJOBS)
		nextjid = 1;
	    strcpy(jobs[i].cmdline, cmdline);
  	    if(verbose){
	        printf("Added job [%d] %d %s\n", jobs[i].jid, jobs[i].pid, jobs[i].cmdline);
            }
            return 1;
	}
    }
    printf("Tried to create too many jobs\n");
    return 0;
}

/* deletejob - Delete a job whose PID=pid from the job list */
int deletejob(struct job_t *jobs, pid_t pid) 
{
    int i;

    if (pid < 1)
	return 0;

    for (i = 0; i < MAXJOBS; i++) {
	if (jobs[i].pid == pid) {
	    clearjob(&jobs[i]);
	    nextjid = maxjid(jobs)+1;
	    return 1;
	}
    }
    return 0;
}

/* fgpid - Return PID of current foreground job, 0 if no such job */
pid_t fgpid(struct job_t *jobs) {
    int i;

    for (i = 0; i < MAXJOBS; i++)
	if (jobs[i].state == FG)
	    return jobs[i].pid;
    return 0;
}

/* getjobpid  - Find a job (by PID) on the job list */
struct job_t *getjobpid(struct job_t *jobs, pid_t pid) {
    int i;

    if (pid < 1)
	return NULL;
    for (i = 0; i < MAXJOBS; i++)
	if (jobs[i].pid == pid)
	    return &jobs[i];
    return NULL;
}

/* getjobjid  - Find a job (by JID) on the job list */
struct job_t *getjobjid(struct job_t *jobs, int jid) 
{
    int i;

    if (jid < 1)
	return NULL;
    for (i = 0; i < MAXJOBS; i++)
	if (jobs[i].jid == jid)
	    return &jobs[i];
    return NULL;
}

/* pid2jid - Map process ID to job ID */
int pid2jid(pid_t pid) 
{
    int i;

    if (pid < 1)
	return 0;
    for (i = 0; i < MAXJOBS; i++)
	if (jobs[i].pid == pid) {
            return jobs[i].jid;
        }
    return 0;
}

/* listjobs - Print the job list */
void listjobs(struct job_t *jobs) 
{
    int i;
    
    for (i = 0; i < MAXJOBS; i++) {
	if (jobs[i].pid != 0) {
	    printf("[%d] (%d) ", jobs[i].jid, jobs[i].pid);
	    switch (jobs[i].state) {
		case BG: 
		    printf("Running ");
		    break;
		case FG: 
		    printf("Foreground ");
		    break;
		case ST: 
		    printf("Stopped ");
		    break;
	    default:
		    printf("listjobs: Internal error: job[%d].state=%d ", 
			   i, jobs[i].state);
	    }
	    printf("%s", jobs[i].cmdline);
	}
    }
}
/******************************
 * end job list helper routines
 ******************************/


/***********************
 * Other helper routines
 ***********************/

/*
 * usage - print a help message
 */
void usage(void) 
{
    printf("Usage: shell [-hvp]\n");
    printf("   -h   print this message\n");
    printf("   -v   print additional diagnostic information\n");
    printf("   -p   do not emit a command prompt\n");
    exit(1);
}

/*
 * unix_error - unix-style error routine
 */
void unix_error(char *msg)
{
    fprintf(stdout, "%s: %s\n", msg, strerror(errno));
    exit(1);
}

/*
 * app_error - application-style error routine
 */
void app_error(char *msg)
{
    fprintf(stdout, "%s\n", msg);
    exit(1);
}

/*
 * Signal - wrapper for the sigaction function
 */
handler_t *Signal(int signum, handler_t *handler) 
{
    struct sigaction action, old_action;

    action.sa_handler = handler;  
    sigemptyset(&action.sa_mask); /* block sigs of type being handled */
    action.sa_flags = SA_RESTART; /* restart syscalls if possible */

    if (sigaction(signum, &action, &old_action) < 0)
	unix_error("Signal error");
    return (old_action.sa_handler);
}

/*
 * sigquit_handler - The driver program can gracefully terminate the
 *    child shell by sending it a SIGQUIT signal.
 */
void sigquit_handler(int sig) 
{
    printf("Terminating after receipt of SIGQUIT signal\n");
    exit(1);
}




