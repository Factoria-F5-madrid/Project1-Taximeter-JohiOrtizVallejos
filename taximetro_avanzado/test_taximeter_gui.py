import unittest
from unittest import mock
import tkinter as tk
from taximeter_gui import TaximeterGUI
from taximeter_cli import Taximeter

class TestTaximeterGUIWithMock(unittest.TestCase):
    @classmethod
    @mock.patch('taximeter_gui.authenticate_gui', return_value=True)
    def setUpClass(cls, mock_auth):
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.gui = TaximeterGUI(cls.root)
        cls.gui.taximeter = Taximeter()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    @mock.patch('tkinter.simpledialog.askstring', return_value='1.23')
    def test_set_manual_prices(self, mock_askstring):
        self.gui.taximeter.price_stopped = 0.02
        self.gui.taximeter.price_moving = 0.05
        self.gui.taximeter.current_fare = "manual"
        self.gui.taximeter.price_stopped = float(mock_askstring())
        self.gui.taximeter.price_moving = float(mock_askstring())
        self.assertEqual(self.gui.taximeter.price_stopped, 1.23)
        self.assertEqual(self.gui.taximeter.price_moving, 1.23)

    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch('tkinter.simpledialog.askstring', side_effect=['usuario', 'contraseña'])
    @mock.patch('taximeter_gui.auth.create_user', return_value=True)
    def test_create_user_dialog(self, mock_create_user, mock_askstring, mock_showinfo):
        self.gui.dev_menu()
        mock_create_user.assert_not_called()

    @mock.patch('tkinter.messagebox.showinfo')
    def test_update_status_messagebox(self, mock_showinfo):
        self.gui.update_status("Mensaje de prueba")
        self.assertIn("Mensaje de prueba", self.gui.status_label.cget("text"))

    @mock.patch('taximeter_gui.auth.load_user', return_value={'User': 'Password'})
    @mock.patch('taximeter_gui.messagebox.showerror')
    @mock.patch('taximeter_gui.messagebox.showinfo')
    @mock.patch('taximeter_gui.LoginWindow')
    def test_authenticate_gui_success(self, mock_loginwindow, mock_showinfo, mock_showerror, mock_load_user):
        # Simula autenticación exitosa: usuario y contraseña coinciden
        instance = mock_loginwindow.return_value
        instance.result = ('User', 'Password')
        from taximeter_gui import authenticate_gui
        self.assertTrue(authenticate_gui())
        mock_showinfo.assert_called()
        mock_showerror.assert_not_called()

if __name__ == '__main__':
    unittest.main()
