using System;
using System.Drawing;
using System.Windows.Forms;

namespace LayOn
{
    public partial class Form1 : Form
    {
        private Bitmap firstImage;
        private Bitmap secondImage;
        private PictureBox pictureBox2 = new PictureBox();

        public Form1()
        {
            InitializeComponent();

            // Инициализируем pictureBox2
            pictureBox2.SizeMode = PictureBoxSizeMode.AutoSize;
            pictureBox2.Visible = false;
            Controls.Add(pictureBox2);
        }

        private Bitmap OverlayImages(Bitmap firstImage, Bitmap secondImage)
        {
            int width = firstImage.Width;
            int height = firstImage.Height;

            Bitmap overlayedImage = new Bitmap(width, height);

            // Определяем область перекрытия изображений
            int startX = Math.Max(0, pictureBox2.Location.X - pictureBox1.Location.X);
            int startY = Math.Max(0, pictureBox2.Location.Y - pictureBox1.Location.Y);
            int endX = Math.Min(firstImage.Width, pictureBox2.Location.X - pictureBox1.Location.X + secondImage.Width);
            int endY = Math.Min(firstImage.Height, pictureBox2.Location.Y - pictureBox1.Location.Y + secondImage.Height);

            // Обходим область перекрытия и настраиваем пиксели наложенного изображения
            for (int y = startY; y < endY; y++)
            {
                for (int x = startX; x < endX; x++)
                {
                    Color secondColor = secondImage.GetPixel(x - pictureBox2.Location.X, y - pictureBox2.Location.Y);

                    Color firstColor = firstImage.GetPixel(x, y);

                    int avgR = (firstColor.R + secondColor.R) / 2;
                    int avgG = (firstColor.G + secondColor.G) / 2;
                    int avgB = (firstColor.B + secondColor.B) / 2;

                    overlayedImage.SetPixel(x, y, Color.FromArgb(avgR, avgG, avgB));
                }
            }

            // Копируем оставшуюся часть первого изображения без изменений
            for (int y = 0; y < firstImage.Height; y++)
            {
                for (int x = 0; x < firstImage.Width; x++)
                {
                    if (x < startX || x >= endX || y < startY || y >= endY)
                    {
                        overlayedImage.SetPixel(x, y, firstImage.GetPixel(x, y));
                    }
                }
            }

            return overlayedImage;
        }


        private Color GetPixelColor(Bitmap image, int x, int y)
        {
            // Проверяем, находится ли точка в пределах изображения
            if (x >= 0 && x < image.Width && y >= 0 && y < image.Height)
            {
                // Если да, возвращаем цвет пикселя
                return image.GetPixel(x, y);
            }
            else
            {
                // Если точка находится за пределами изображения, возвращаем цвет прозрачности
                return Color.Transparent;
            }
        }

        private void pictureBox1_MouseClick(object sender, MouseEventArgs e)
        {
            if (secondImage != null)
            {
                // Получаем координаты клика
                int clickX = e.X;
                int clickY = e.Y;

                // Устанавливаем позицию pictureBox2 относительно pictureBox1
                pictureBox2.Location = new Point(clickX, clickY);
                pictureBox2.Visible = true;

                // Создаем наложенное изображение
                Bitmap overlaidImage = OverlayImages(firstImage, secondImage);

                // Отображаем наложенное изображение на pictureBox1
                pictureBox1.Image = overlaidImage;
            }
            else
            {
                MessageBox.Show("Сначала выберите изображение для наложения.");
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            OpenFileDialog fb = new OpenFileDialog();
            fb.Filter = "jpg|*.jpg";
            pictureBox1.SizeMode = PictureBoxSizeMode.AutoSize;
            if (fb.ShowDialog() == DialogResult.OK)
            {
                firstImage = new Bitmap(fb.FileName);
                pictureBox1.Image = firstImage;
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            OpenFileDialog fb = new OpenFileDialog();
            fb.Filter = "jpg|*.jpg";
            pictureBox2.SizeMode = PictureBoxSizeMode.AutoSize;
            if (fb.ShowDialog() == DialogResult.OK)
            {
                secondImage = new Bitmap(fb.FileName);
                pictureBox2.Image = secondImage;
            }
        }
    }
}
