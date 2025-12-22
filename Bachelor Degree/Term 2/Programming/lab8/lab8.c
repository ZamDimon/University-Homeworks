#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define _CRT_SECURE_NO_WARNINGS
#define MAX_NUMBER_EMPLOYEES 50
#define MAX_NAME_LENGTH 20
#define MAX_LINE_LENGTH 50

#define FLOAT_ERROR 0.0001f
#define ADD_EMPLOYEE_MODE 0
#define PRINT_EMPLOYEES_MODE 1
#define SAVE_EMPLOYEES_MODE 2
#define EXIT_MODE 3

// Define person struct
struct Person
{
    char name[MAX_NAME_LENGTH];
    int age;
    float salary;
};

// Define employees list
struct EmployeesList
{
    struct Person employees[MAX_NUMBER_EMPLOYEES];
    int currentNumber;
};

// Define print person function
void printPerson(struct Person person)
{
    printf("Name: %s | Age: %3d | Salary: %10.2f \n", person.name, person.age, person.salary);
}

// Define the function that specifies whether the person is default or not
int defaultPerson(struct Person person)
{
    return (strcmp(person.name, "") == 0 && (person.age == 0) && (person.salary - 0.0f) <= FLOAT_ERROR)? 1 : 0;
}

// Define read person function
void readPerson(struct Person *personToAdd)
{
    printf("Type in the name: ");
    getchar();
    gets(personToAdd->name);
    printf("Type in the age: ");
    scanf("%d", &personToAdd->age);
    printf("Type in the salary: ");
    scanf("%f", &personToAdd->salary);
}

// Define write person to the file function
void fileWritePerson(struct Person person, char fileName[MAX_NAME_LENGTH])
{
    FILE *file;
    file = fopen(fileName, "a"); // Using "a" for overwriting the file
    fprintf(file, "%s\n", person.name);
    fprintf(file, "%d\n", person.age);
    fprintf(file, "%f\n", person.salary);
    fclose(file);
}

// Define add employee function
void addEmployee(struct EmployeesList *list, struct Person person)
{
    list->employees[list->currentNumber] = person;
    list->currentNumber++;
}

// Define print employees list function
void printEmployees(struct EmployeesList list)
{
    for (int i = 0; i < list.currentNumber; ++i)
    {
        printPerson(list.employees[i]);
    }
}

// Define save employees to the file function
void saveEmployees(struct EmployeesList list, char fileName[MAX_NAME_LENGTH])
{
    FILE* textFile;
    textFile = fopen(fileName, "r");
    if (textFile != NULL)
    {
        fclose(fopen(fileName, "w")); // Clear the file if it does exist
    }

    for (int i = 0; i < list.currentNumber; ++i)
    {
        fileWritePerson(list.employees[i], fileName);
    }
}

int defaultEmployees(struct EmployeesList employeesList)
{
    return (employeesList.currentNumber <= 1 && defaultPerson(employeesList.employees[0]) == 1)? 1 : 0;
}

// Define employees loading operation
void loadEmployees(struct EmployeesList *list, char fileName[MAX_NAME_LENGTH])
{
    FILE *textFile;
    char line[MAX_NAME_LENGTH];

    // Define and open the file
    textFile = fopen(fileName, "r");

    // Read line by line
    struct Person personToAdd = {"", 0, 0.0f}; // Struct of a person that we add by iterating over txt file
    int lineNumber = 0; // Line number

    while (fgets(line, MAX_NAME_LENGTH, textFile))
    {
        switch (lineNumber % 3) {
            case 0:
                if (lineNumber != 0)
                {
                    addEmployee(list, personToAdd);
                }

                strcpy(personToAdd.name, line);
            case 1:
                personToAdd.age = atoi(line);
            case 2:
                personToAdd.salary = atof(line);
        }

        lineNumber++;
    }

    addEmployee(list, personToAdd);
    fclose(textFile);

    return;
}

//Returns 1 if number of elements in the employees list equals or exceeds maximum number of elements
int exceedsMaxEmployees(struct EmployeesList list)
{
    return (list.currentNumber >= MAX_NUMBER_EMPLOYEES)? 1 : 0;
}

void clearTerminal()
{
    system("clear"); // Had to change this line since I am using Linux
}

void waitForPressAnyKey()
{
    printf("Press any key to continue\n");
    getchar();
    getchar();
}

int main()
{
    // Define employees list
    struct EmployeesList employeesList;

    printf("%d", employeesList.currentNumber);

    char employeesFile[MAX_NAME_LENGTH] = "employees.txt";
    int running = 1; // 1 if the program is running and 0 otherwise

    // Try to load a list
    FILE *textFile;
    textFile = fopen(employeesFile, "r");
    if (textFile == NULL) {
        printf("Failed to find file employees.txt. Proceed to the program?\n");
        waitForPressAnyKey();
    }
    else {
        struct EmployeesList tempList;
        loadEmployees(&tempList, employeesFile);
        if (defaultEmployees(tempList)) {
            printf("File is empty. Proceed to the program?\n");
            getchar();
        }
        else {
            employeesList = tempList;
        }
    }

    while(running)
    {
        // Clear the terminal
        clearTerminal();

        // Read selected mode
        int selectedMode = 0;
        printf("Select one of the following modes:\n0 - Add employee\n1 - Print employees list\n2 - Save employees list\n3 - Exit\n");
        scanf("%d", &selectedMode);

        switch(selectedMode) {
            case ADD_EMPLOYEE_MODE:
                clearTerminal();

                if (exceedsMaxEmployees(employeesList))
                {
                    // If the maximum number of employees is exceeded, abort the operation
                    printf("You cannot add new employee due to the limit\n");
                    waitForPressAnyKey();
                    break;
                }

                // Initialize struct that will be further added to the list
                struct Person personToAdd;
                // Reading a person
                readPerson(&personToAdd);
                // Adding this person to the list
                addEmployee(&employeesList, personToAdd);
                waitForPressAnyKey();
                break;
            case PRINT_EMPLOYEES_MODE:
                // Just print out all the employees
                clearTerminal();
                printf("--List of employees--\n");
                printEmployees(employeesList);
                waitForPressAnyKey();
                break;
            case SAVE_EMPLOYEES_MODE:
                clearTerminal();
                // Save all the employees
                saveEmployees(employeesList, employeesFile);
                printf("Operation succeeded\n");
                waitForPressAnyKey();
                break;
            case EXIT_MODE:
                // Exit the program
                running = 0;
                break;
            default:
                clearTerminal();
                printf("Specified mode does not exist\n");
                waitForPressAnyKey();
                break;
        }
    }
}


