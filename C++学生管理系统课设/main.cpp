/**
 * @file main.cpp
 * @brief 学生成绩管理系统主程序文件
 * @author 龚洙淋　叶子芊　赵羽欣
 * @date 2026年
 * @copyright 版权所有 © 2026 学生成绩管理系统
 */

#include "manageinfo.h"
#include "colors.h"
#include "utils.h"
#include <windows.h>
#include <iostream>
#include <string>

const std::string DATA_FILE = "result.txt";

/**
 * @namespace StudentManagement
 * @brief 学生成绩管理系统命名空间
 */
using namespace StudentManagement;

// 常量定义
constexpr const char* SAVE_FILE_NAME = "result.txt"; ///< 学生信息保存文件名
constexpr int CONTINUE_PROGRAM = 1;                   ///< 程序继续运行码

/**
 * @brief 设置控制台编码为UTF-8
 * @details 确保控制台能够正确显示中文等非ASCII字符
 */
void setConsoleUTF8() {
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
}

/**
 * @brief 打印系统标题
 * @return 操作结果码
 */
int printTitle() {
    std::cout << "\n";
    std::cout << Colors::BG_BRIGHT_BLUE << Colors::WHITE << Colors::BOLD;
    std::cout << "*******************************************" << std::endl;
    std::cout << "*                                         *" << std::endl;
    std::cout << "*          学生成绩管理系统               *" << std::endl;
    std::cout << "*                                         *" << std::endl;
    std::cout << "*******************************************" << std::endl;
    std::cout << Colors::RESET;
    return 0;
}

/**
 * @brief 打印操作菜单
 * @return 用户选择的操作编号
 */
/**
 * @brief 打印学生信息管理子菜单
 * @return 用户选择的操作编号
 */
int printStudentManagementSubMenu() {
    std::cout << Colors::BOLD << Colors::BRIGHT_GREEN << "学生信息管理" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "1. " << Colors::WHITE << "录入学生信息" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "2. " << Colors::WHITE << "修改学生信息" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "3. " << Colors::WHITE << "删除学生信息" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "0. " << Colors::WHITE << "返回主菜单" << Colors::RESET << std::endl;
    std::cout << "\n" << Colors::BRIGHT_YELLOW << "请输入选择：" << Colors::RESET;
    
    int choice;
    std::cin >> choice;
    return choice;
}

/**
 * @brief 打印学生信息查询子菜单
 * @return 用户选择的操作编号
 */
int printStudentQuerySubMenu() {
    std::cout << Colors::BOLD << Colors::BRIGHT_BLUE << "学生信息查询" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "1. " << Colors::WHITE << "查看所有学生信息" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "2. " << Colors::WHITE << "按学号查询学生信息" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "3. " << Colors::WHITE << "查询成绩及格的学生" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "4. " << Colors::WHITE << "查找成绩最高的学生" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "0. " << Colors::WHITE << "返回主菜单" << Colors::RESET << std::endl;
    std::cout << "\n" << Colors::BRIGHT_YELLOW << "请输入选择：" << Colors::RESET;
    
    int choice;
    std::cin >> choice;
    return choice;
}

/**
 * @brief 打印学生信息排序子菜单
 * @return 用户选择的操作编号
 */
int printStudentSortSubMenu() {
    std::cout << Colors::BOLD << Colors::BRIGHT_MAGENTA << "学生信息排序" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "1. " << Colors::WHITE << "按学号排序学生信息" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "2. " << Colors::WHITE << "按成绩排序学生信息" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "0. " << Colors::WHITE << "返回主菜单" << Colors::RESET << std::endl;
    std::cout << "\n" << Colors::BRIGHT_YELLOW << "请输入选择：" << Colors::RESET;
    
    int choice;
    std::cin >> choice;
    return choice;
}

/**
 * @brief 打印系统管理子菜单
 * @return 用户选择的操作编号
 */
int printSystemManagementSubMenu() {
    std::cout << Colors::BOLD << Colors::BRIGHT_YELLOW << "系统管理" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "1. " << Colors::WHITE << "保存学生信息到文件" << Colors::RESET << std::endl;
    std::cout << Colors::CYAN << "0. " << Colors::WHITE << "返回主菜单" << Colors::RESET << std::endl;
    std::cout << "\n" << Colors::BRIGHT_YELLOW << "请输入选择：" << Colors::RESET;
    
    int choice;
    std::cin >> choice;
    return choice;
}

/**
 * @brief 打印主菜单
 * @return 用户选择的操作编号
 */
int printMenu() {
    std::cout << Colors::BOLD << Colors::BRIGHT_WHITE << "主菜单：" << Colors::RESET << std::endl;
    std::cout << Colors::BRIGHT_GREEN << "1. " << Colors::WHITE << "学生信息管理" << Colors::RESET << std::endl;
    std::cout << Colors::BRIGHT_BLUE << "2. " << Colors::WHITE << "学生信息查询" << Colors::RESET << std::endl;
    std::cout << Colors::BRIGHT_MAGENTA << "3. " << Colors::WHITE << "学生信息排序" << Colors::RESET << std::endl;
    std::cout << Colors::BRIGHT_YELLOW << "4. " << Colors::WHITE << "系统管理" << Colors::RESET << std::endl;
    std::cout << Colors::BRIGHT_RED << "0. " << Colors::WHITE << "退出系统" << Colors::RESET << std::endl;
    std::cout << "\n" << Colors::BRIGHT_YELLOW << "请输入选择：" << Colors::RESET;
    
    int choice;
    std::cin >> choice;
    return choice;
}



/**
 * @brief 处理学生信息管理子菜单选择
 * @param choice 用户选择的操作编号
 * @param manager 学生信息管理对象
 */
void handleStudentManagementSubMenu(int choice, Manageinfo& manager) {
    switch (choice) {
        case 1: { // 录入学生信息
            Student stu;
            std::cin >> stu;
            manager.insert_stu(stu);
            break;
        }
        case 2: // 修改学生信息
            manager.modify_student();
            Utils::WaitForKey();
            break;
        case 3: // 删除学生信息
            manager.delete_student();
            Utils::WaitForKey();
            break;
        case 0: // 返回主菜单
            return;
        default: // 无效选择
            std::cout << Colors::BRIGHT_RED << "无效的选择，请重新输入！" << Colors::RESET << std::endl;
            Utils::WaitForKey();
            break;
    }
}

/**
 * @brief 处理学生信息查询子菜单选择
 * @param choice 用户选择的操作编号
 * @param manager 学生信息管理对象
 */
void handleStudentQuerySubMenu(int choice, Manageinfo& manager) {
    switch (choice) {
        case 1: // 查看所有学生信息
            manager.list_student();
            Utils::WaitForKey();
            break;
        case 2: // 按学号查询学生信息
            manager.search_id();
            Utils::WaitForKey();
            break;
        case 3: // 查询成绩及格的学生
            manager.search_grade_pass();
            Utils::WaitForKey();
            break;
        case 4: // 查找成绩最高的学生
            manager.find_highest_grade();
            Utils::WaitForKey();
            break;
        case 0: // 返回主菜单
            return;
        default: // 无效选择
            std::cout << Colors::BRIGHT_RED << "无效的选择，请重新输入！" << Colors::RESET << std::endl;
            Utils::WaitForKey();
            break;
    }
}

/**
 * @brief 处理学生信息排序子菜单选择
 * @param choice 用户选择的操作编号
 * @param manager 学生信息管理对象
 */
void handleStudentSortSubMenu(int choice, Manageinfo& manager) {
    switch (choice) {
        case 1: // 按学号排序学生信息
            manager.sort_by_id();
            Utils::WaitForKey();
            break;
        case 2: // 按成绩排序学生信息
            manager.sort_by_grade();
            Utils::WaitForKey();
            break;
        case 0: // 返回主菜单
            return;
        default: // 无效选择
            std::cout << Colors::BRIGHT_RED << "无效的选择，请重新输入！" << Colors::RESET << std::endl;
            Utils::WaitForKey();
            break;
    }
}

/**
 * @brief 处理系统管理子菜单选择
 * @param choice 用户选择的操作编号
 * @param manager 学生信息管理对象
 */
void handleSystemManagementSubMenu(int choice, Manageinfo& manager) {
    switch (choice) {
        case 1: // 保存学生信息到文件
            manager.save_students_to_file(SAVE_FILE_NAME);
            Utils::WaitForKey();
            break;
        case 0: // 返回主菜单
            return;
        default: // 无效选择
            std::cout << Colors::BRIGHT_RED << "无效的选择，请重新输入！" << Colors::RESET << std::endl;
            Utils::WaitForKey();
            break;
    }
}

/**
 * @brief 处理用户选择的操作
 * @param choice 用户选择的操作编号
 * @param manager 学生信息管理对象
 * @return 操作结果码：0表示退出系统，1表示继续运行
 */
int handleChoice(int choice, Manageinfo& manager) {
    // 保存退出选项，不执行清屏
    if (choice == 0) {
        std::cout << Colors::BRIGHT_GREEN << "感谢使用学生成绩管理系统！" << Colors::RESET << std::endl;
        return EXIT_SUCCESS;
    }
    
    bool continueSubMenu;
    
    switch (choice) {
        case 1: // 学生信息管理
            do {
                Utils::ClearScreen();
                printTitle();
                int subChoice = printStudentManagementSubMenu();
                
                if (subChoice == 0) {
                    continueSubMenu = false;
                } else {
                    Utils::ClearScreen();
                    printTitle();
                    handleStudentManagementSubMenu(subChoice, manager);
                    continueSubMenu = true;
                }
            } while (continueSubMenu);
            break;
            
        case 2: // 学生信息查询
            do {
                Utils::ClearScreen();
                printTitle();
                int subChoice = printStudentQuerySubMenu();
                
                if (subChoice == 0) {
                    continueSubMenu = false;
                } else {
                    Utils::ClearScreen();
                    printTitle();
                    handleStudentQuerySubMenu(subChoice, manager);
                    continueSubMenu = true;
                }
            } while (continueSubMenu);
            break;
            
        case 3: // 学生信息排序
            do {
                Utils::ClearScreen();
                printTitle();
                int subChoice = printStudentSortSubMenu();
                
                if (subChoice == 0) {
                    continueSubMenu = false;
                } else {
                    Utils::ClearScreen();
                    printTitle();
                    handleStudentSortSubMenu(subChoice, manager);
                    continueSubMenu = true;
                }
            } while (continueSubMenu);
            break;
            
        case 4: // 系统管理
            do {
                Utils::ClearScreen();
                printTitle();
                int subChoice = printSystemManagementSubMenu();
                
                if (subChoice == 0) {
                    continueSubMenu = false;
                } else {
                    Utils::ClearScreen();
                    printTitle();
                    handleSystemManagementSubMenu(subChoice, manager);
                    continueSubMenu = true;
                }
            } while (continueSubMenu);
            break;
            
        default: // 无效选择
            std::cout << Colors::BRIGHT_RED << "无效的选择，请重新输入！" << Colors::RESET << std::endl;
            Utils::WaitForKey();
            break;
    }

    Utils::ClearScreen(); // 清屏
    printTitle(); // 重新打印标题

    return CONTINUE_PROGRAM;
}

/**
 * @brief 程序初始化
 */
Manageinfo init(){
    setConsoleUTF8(); // 设置控制台编码为UTF-8
    Manageinfo manager(DATA_FILE); // 创建学生信息管理对象，自动读取文件
    return manager;
}


/**
 * @brief 程序主函数
 * @return 程序退出码
 */
int main() {
    Manageinfo manager = init();//程序初始化
    Utils::ClearScreen(); // 清屏
    int choice;         // 用户选择的操作编号
    printTitle(); // 打印系统标题
    
    do {
        choice = printMenu(); // 打印菜单并获取用户选择
    } while (handleChoice(choice, manager) != EXIT_SUCCESS); // 无限循环，直到用户选择退出
    
    // 自动保存文件到指定路径
    manager.save_students_to_file(DATA_FILE);
    return EXIT_SUCCESS;
}
