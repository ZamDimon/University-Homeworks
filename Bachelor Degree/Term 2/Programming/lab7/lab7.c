#include <stdio.h>
#define MAX_NUMBER_EMPLOYEES 2
#define MAX_NAME_LENGTH 20

#define ADD_EMPLOYEE_MODE 0
#define PRINT_EMPLOYEES_MODE 1
#define EXIT_MODE 2

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

//Returns 1 if number of elements in the employees list equals or exceeds maximum number of elements
int exceedsMaxEmployees(struct EmployeesList list)
{
    return (list.currentNumber >= MAX_NUMBER_EMPLOYEES)? 1 : 0;
}

// To test basic functionality you can call this function
void Test()
{
    // Define employees list
    struct EmployeesList employeesList;

    printf("Defined people:\n");
    // Define 2 people and print them out
    struct Person person1 = {"Doe", 20, 5000};
    printPerson(person1);
    struct Person person2 = {"Dmytro", 18, 40000};
    printPerson(person2);

    printf("Employees list:\n");
    // Add these 2 people to the list
    addEmployee(&employeesList, person1);
    addEmployee(&employeesList, person2);

    // Print the whole array
    printEmployees(employeesList);
    return;
}

int main()
{
    // Define employees list
    struct EmployeesList employeesList;
    int running = 1; // 1 if the program is running and 0 otherwise
    while(running)
    {
        // Read selected mode
        int selectedMode = 0;
        printf("Select one of the following modes:\n0 - Add employee\n1 - Print employees list\n2 - Exit\n");
        scanf("%d", &selectedMode);

        switch(selectedMode) {
            case ADD_EMPLOYEE_MODE:
                if (exceedsMaxEmployees(employeesList))
                {
                    // If the maximum number of employees is exceeded, abort the operation
                    printf("You cannot add new employee due to the limit\n");
                    break;
                }

                // Initialize struct that will be further added to the list
                struct Person personToAdd;
                // Reading a person
                readPerson(&personToAdd);
                // Adding this person to the list
                addEmployee(&employeesList, personToAdd);
                break;
            case PRINT_EMPLOYEES_MODE:
                // Just print out all the employees
                printEmployees(employeesList);
                break;
            case EXIT_MODE:
                // Exit the program
                running = 0;
                break;
        }
    }
}

