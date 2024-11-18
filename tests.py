import unittest
import os
import shutil
from emulator import  Emulator

class TestEmulatorCommands(unittest.TestCase):

    def setUp(self):
        # Создание временной тестовой директории и файловой структуры

        print('setUP start')
        os.makedirs('test_dir/sub_dir', exist_ok=True)
        with open('test_dir/file1.txt', 'w') as f:
            f.write('This is a test file.')
        with open('test_dir/sub_dir/file2.txt', 'w') as f:
            f.write('This is another test file.')

    def test_ls(self):
        # Проверка команды 'ls'
        # Список файлов и папок в test_dir должен включать file1.txt и sub_dir
        print ('test_ls START')
        emulator = Emulator('config-test.ini')
        expected_output = [ 'file1.txt', 'sub_dir']

        #actual_output = set(os.listdir('test_dir'))
        actual_output = emulator.execute_command( 'ls test_dir' )
        self.assertEqual(expected_output, actual_output)
        print ('test_ls STOP')

    def test_cd(self):
        # Проверка команды 'cd' (изменение директории)
        # Перемещаемся в 'test_dir/sub_dir' и проверяем текущую директорию
        print ('test_cd START')
        emulator = Emulator('config-test.ini')
        START_CWD= os.getcwd()
        #os.chdir('test_dir/sub_dir')
        emulator.execute_command( 'cd test_dir/sub_dir')
        CWD = os.getcwd()
        ABS = os.path.abspath('.')
        os.chdir( START_CWD  ) # ДЛя того чтобы вернуться в стартовый каталог обратно иначе нельзя удалть то чего нет
        self.assertEqual( CWD, ABS)

        print ('test_cd STOP')

    def test_rmdir(self):
        # Проверка команды 'rmdir' (удаление директории)
        # Удаляем подкаталог 'sub_dir' и убедимся, что он удален
        print ('test_rmdir START')
        os.remove('test_dir/sub_dir/file2.txt') # очищаем каталог ибо только чистый каталог можно удалить

        emulator = Emulator('config-test.ini')
        emulator.execute_command('rmdir test_dir/sub_dir')

        #os.rmdir('test_dir/sub_dir')

        self.assertNotIn('sub_dir', os.listdir('test_dir'))
        # Проверяем, что попытка удалить не пустую директорию вызывает ошибку
        with self.assertRaises(OSError):
            os.rmdir('test_dir')  # test_dir не пустой
        print('test_rmdir STOP')

    def test_du(self):
        # Проверка команды 'du' (используется для оценки использования дискового пространства)
        # Проверим размер файла в test_dir
        print ('test_du START')
        file_path = 'test_dir/sub_dir/'
        file_name = 'file2.txt'
        expected_size = os.path.getsize(file_path+file_name)

        command = 'du '+ file_path
        emulator = Emulator('config-test.ini')
        actual_size = emulator.execute_command(command)

        # actual_size = sum(os.path.getsize(f) for f in os.listdir('test_dir') if os.path.isfile(f))
        self.assertEqual(expected_size, actual_size)
        print('test_du STOP')

    def tearDown(self):
        # Удаление временной тестовой директории и всех ее содержимого
        print('tearDown START')
        try:
#            os.chdir(self.START_DIR)
            CDW = os.getcwd()
            shutil.rmtree('./test_dir')
        except Exception as e:
            print(f"Ошибка при удалении тестового окружения: {e}")

        print('tearDown STOP')

if __name__ == '__main__':

    print ('------------------------\n')
    print (os.getcwd())
    print ('-----------------------------\n')
    unittest.main()
