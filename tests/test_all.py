from unittest import TestCase
from main import main
import subprocess
from subprocess import Popen, PIPE

OUTPUT_DIR = "tests/dest/"


def build(file_name: str) -> int:
    with open(f"tests/src/{file_name}.txt", "rb") as f:
        text = str(f.read())[2:-1]  # trims b'str' to str
    path = OUTPUT_DIR + f"{file_name}.cpp"
    main(text, path, test=True)
    subprocess.run(f"g++ -masm=intel tests/dest/{file_name}.cpp -o tests/exec/{file_name}".split(" "))

    p = Popen([f"./tests/exec/{file_name}"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    res = int(output.decode("utf-8"))
    return res


class Test1(TestCase):

    def test_01(self):
        res = build("test_01")
        self.assertEqual(res, 8)

    def test_02(self):
        res = build("test_02")
        self.assertEqual(res, -2)

    def test_03(self):
        res = build("test_03")
        self.assertEqual(res, 1)

    def test_04(self):
        res = build("test_04")
        self.assertEqual(res, -20)

    def test_05(self):
        res = build("test_05")
        self.assertEqual(res, 100)

    def test_06(self):
        res = build("test_06")
        self.assertEqual(res, -12340000)

    def test_07(self):
        res = build("test_07")
        self.assertEqual(res, 135)

    def test_08(self):
        res = build("test_08")
        self.assertEqual(res, -12)
