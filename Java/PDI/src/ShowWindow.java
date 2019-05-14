

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */


import java.awt.BorderLayout;
import java.awt.Container;
import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.awt.image.DataBufferByte;
import java.util.ArrayList;
import javax.swing.*;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
//para a riação dos gráficos
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartFrame;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;
import org.jfree.data.general.DefaultPieDataset;


/**
 *
 * @author Danilo - Modificada por José Carlos
 */
public class ShowWindow extends JFrame{
    public static JFrame frame;
    public static Mat picture;  
    public static BufferedImage image;
    public static int larg;
    public static int alt;
    public static int modo;
    

  
    public static void showWindow(String nomeJanela, Mat picture){
        frame = new JFrame(nomeJanela);
       // frame = new JInternalFrame(nomeJanela);
        frame.setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);
        frame.setSize(300, 300);//largura e altura
        frame.setLocationRelativeTo(null);
        
        image = matToBufferedImage(picture);
        JPanel panel = new JPanel(){
        @Override
        public void paintComponent(Graphics g) {
            //BufferedImage image = null; // get your buffered image.
            //Graphics2D graphics2d = (Graphics2D) g;
            //graphics2d.drawImage(image, 0, 0, null);
            g.drawImage(image,0,0,frame.getWidth(),frame.getHeight(), this);
            super.paintComponents(g);
            
        }
    };
        frame.setContentPane(panel);
        frame.setVisible(true);
        
    }
    
    
    public static void showWindow(String nomeJanela, Mat picture, int l, int a){
        frame = new JFrame(nomeJanela);
        frame.setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);
        frame.setSize(l,a);//largura e altura
        frame.setLocationRelativeTo(null);
        image = matToBufferedImage(picture);
        if(l == 0){alt = image.getHeight(); larg = image.getWidth();}
        larg = l;
        alt = a;
        JPanel panel = new JPanel(){
        @Override
        public void paintComponent(Graphics g) {
             g.drawImage(image,0,0,larg,alt, this);
             super.paintComponents(g);    
        }
    };
        frame.setContentPane(panel);
        frame.setVisible(true);
    }
    
    
    /**  
    * Converts/writes a Mat into a BufferedImage.  
    *  
    * @param matrix Mat of type CV_8UC3 or CV_8UC1  
    * @return BufferedImage of type TYPE_3BYTE_BGR or TYPE_BYTE_GRAY  
    */  
   public static BufferedImage matToBufferedImage(Mat matrix) {  
     int cols = matrix.cols();  
     int rows = matrix.rows();  
     int elemSize = (int)matrix.elemSize();  
     byte[] data = new byte[cols * rows * elemSize];  
     int type;  
     matrix.get(0, 0, data);  
     switch (matrix.channels()) {  
       case 1:  
         type = BufferedImage.TYPE_BYTE_GRAY;  
         break;  
       case 3:  
         type = BufferedImage.TYPE_3BYTE_BGR;  
         // bgr to rgb  
         byte b;  
         for(int i=0; i<data.length; i=i+3) {  
           b = data[i];  
           data[i] = data[i+2];  
           data[i+2] = b;  
         }  
         break;  
       default:  
         return null;  
     }  
     BufferedImage image = new BufferedImage(cols, rows, type);  
     image.getRaster().setDataElements(0, 0, cols, rows, data);  
     return image;  
   }  
   
   //Converte de BufferedImag para Mat
  public static Mat bufferedImageToMat(BufferedImage bi) {
      
  if (bi.getType() == BufferedImage.TYPE_BYTE_GRAY){    
    Mat mat = new Mat(bi.getHeight(), bi.getWidth(), CvType.CV_8UC1);
    byte[] data = ((DataBufferByte) bi.getRaster().getDataBuffer()).getData();
   mat.put(0, 0, data);
   return mat;
  } 
  if (bi.getType() == BufferedImage.TYPE_3BYTE_BGR){    
    Mat mat = new Mat(bi.getHeight(), bi.getWidth(), CvType.CV_8UC3);
    byte[] data = ((DataBufferByte) bi.getRaster().getDataBuffer()).getData();
  mat.put(0, 0, data);
  return mat;
  }
        return null;
   
}
  
     //Método para normalizar as imagens
    public static Mat normalizaImagem(double v[], Mat m1){ //Recebe um vetor e uma matriz
        
         //Escala de cinza
            double fmax=-1000000000; double fmin=1000000000;
            
            for (int i=0; i<v.length; i++){

                if(v[i] > fmax){ //Maior
                    fmax=v[i];
                }
                if(v[i] < fmin){ //Menor
                    fmin=v[i];
                }
            }
             
            for (int i=0; i<v.length; i++){

                 v[i] = (255 /(fmax -fmin))*(v[i] - fmin); //Função de normalização
            }
            
        Mat Result = new Mat(m1.rows(), m1.cols(), CvType.CV_8UC1); //Cria a matriz pra receber o resutlado
        Result.put(0, 0, v);

        return Result; //Retorna a matriz
    }  
     
    //Método para transformar as imagens linearmente, contraste
    public static Mat trasnfLinear(double GMax, double GMin, double v[], Mat m1, int t){ //Recebe um vetor e uma matriz
        
         //Escala de cinza
            double fmax=-1000000; double fmin=1000000;
            
            for (int i=0; i<v.length; i++){

                if(v[i] > fmax){ //Maior
                    fmax=v[i];
                }
                if(v[i] < fmin){ //Menor
                    fmin=v[i];
                }
            }
             
                for (int i=0; i<v.length; i++){
                    if (t == 0){
                         v[i] = ((GMax - GMin)/(fmax -fmin))*(v[i] - fmin)+GMin; //Transformação linear
                    }
                    if (t == 1){
                        if (v[i]>=0 && v[i]<=85){
                           v[i] = ((GMax - GMin)/(fmax -fmin))*(v[i] - fmin)+GMin;   
                         }
                         if (v[i]>=86 && v[i]<=170){
                           v[i] = ((GMax - GMin)/(fmax -fmin))*(v[i] - fmin)+GMin+20;   
                         }
                         if (v[i]>=171 && v[i]<=255){
                           v[i] = ((GMax - GMin)/(fmax -fmin))*(v[i] - fmin)+GMin+40;   
                         }
                    }
                }
        Mat Result = new Mat(m1.rows(), m1.cols(), CvType.CV_8UC1); //Cria a matriz pra receber o resutlado
         
        Result.put(0,0, v);
        return Result; //Retorna a matriz
    }  
    
    //MÉTODO PARA CRIAÇÃO E EXIBIÇÃO DE GRÁFICOS
    public static void criaGrafico(double v[], boolean legenda){
        //Cria os dados do gráfico
        DefaultCategoryDataset data = new DefaultCategoryDataset();
       
        for (int i=0; i< 256; i++){
             data.addValue(v[i], ""+i, "Pixels"); //Insere o valor do vetor no DataSet         
        }
 
   
        //Cria o grafico e alimenta com os dados
      
        JFreeChart chart = ChartFactory.createBarChart("Histograma de "+jfPrincipal.img1,
                "",
                "Quantidade de pixels",
                data, 
                PlotOrientation.VERTICAL, 
                legenda, //Legenda
                true, 
                true);
        

        // Cria um frame para mostrar o gráfico
        ChartFrame frame = new ChartFrame("Gráfico de Histograma", chart);
        frame.pack();
        frame.setVisible(true);
     
       
        
    }

    
}
