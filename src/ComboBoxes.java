// The main interface for automated spike check project
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.border.LineBorder;
import javax.swing.filechooser.FileSystemView;
import javax.swing.plaf.basic.BasicArrowButton;
import javax.swing.text.MaskFormatter;
import javax.swing.Timer;


import java.io.*;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.concurrent.TimeUnit;

import java.util.Scanner;
import com.fazecast.jSerialComm.*;

class StreamGobbler extends Thread
{
    InputStream is;
    String type;
    
    StreamGobbler(InputStream is, String type)
    {
        this.is = is;
        this.type = type;
    }
    public void run()
    {
        try
        {
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);
            String line=null;
            while ( (line = br.readLine()) != null)
                System.out.println(type + ">" + line);    
            } catch (IOException ioe)
              {
                ioe.printStackTrace();  
              }
    }
}

public class ComboBoxes extends JFrame {

	
	//declare variables
	String[] x_val;
	String[] y_val;

	static JComboBox cb;
	static JComboBox cn;
	static JLabel lab;
	static JDialog offfid;
	static JDialog dia;

	int x_change=0;
	int y_change=0;
	int z_change=0;
	
	//
	int x_cam=0;
	int y_cam=0;
	int z_cam=0;
	
	//
	int fid_cal=0;

	//Offset calibration variables
	
	int x_off;
	int y_off;
	int pos_x_1 = 0;
	int pos_y_1 = 0;
	int pos_x_2 = 0;
	int pos_y_2 = 0;
	int pos_x_3 = 0;
	int pos_y_3 = 0;
	int y_diff = 0;
	int x_diff = 0;
	int x_off_fid1;
	int y_off_fid1;
	int x_off_fid2;
	int y_off_fid2;
	int x_off_fid3;
	int y_off_fid3;
	boolean values;
	//initialize a counter
	int i = 0;
	
	int x_orig = 0;
	int y_orig = 0;
	String z_orig;
	int x_new = 0;
	int y_new = 0;
	int Z_zero = 0;
	int x_average = 0;
	int y_average = 0;
	//
	int z_max=0;
	int x_max=0;
	int y_max=0;
	int z_min=0;
	int x_min=0;
	int y_min=0;

	int fid_x_1=0;
	int fid_y_1=0;
	int fid_x_2=0;
	int fid_y_2=0;
	int fid_x_3=0;
	int fid_y_3=0;
	String[] fid_1=null;
	String[] fid_2=null;
	String[] fid_3=null;

	String dir_out=null;

	static String dire=System.getProperty("user.dir");
	String fid_name="";

	Cursor cusor=new Cursor(Cursor.HAND_CURSOR);
	
		// exit confirmation (yes or no) 
		public void close(JDialog dia) {							
			dia.setDefaultCloseOperation(JDialog.DO_NOTHING_ON_CLOSE);
			dia.addWindowListener(new WindowAdapter() {
				@Override
				public void windowClosing(WindowEvent e) {
					int conf=JOptionPane.showConfirmDialog(null, "Exit program?",
							"Exit confirmation",JOptionPane.YES_NO_OPTION);
					if (conf==JOptionPane.YES_OPTION) {
						//dia.setVisible(false);
						dia.dispose();
					}
				}
			});
		}
		
		// setting position and dimension for panel
		public void set_position(JPanel pan, JComponent comp, int left_int, int top_int) {
			Insets insets = pan.getInsets();
			Dimension size = comp.getPreferredSize();
			comp.setBounds(left_int + insets.left, top_int + insets.top,
					size.width, size.height);
		}

		// check the value of x (modbus max value is 32767)
		public static String[] check_x(int a) {
			String x_val[] = new String[4];
			if (a<0) {
				a=0;
			}
			if (a>75000) {
				a=75000;
			}
			x_val[0]=String.valueOf(a);
			if (a>32767) {
				if (a>65534) {
					x_val[1]="32767";
					x_val[2]="32767";
					x_val[3]=String.valueOf(a-(32767*2));
				}
				else {
					x_val[1]="32767";
					x_val[2]=String.valueOf(a-32767);
					x_val[3]="0";
				}
			}                               
			else if (a<32767) {
				x_val[1]=x_val[0];
				x_val[2]="0";
				x_val[3]="0";
			}
			return x_val;
		}

		// check value of y
		public static String[] check_y(int a) {
			String y_val[] = new String[3];
			if (a<0) {
				a=0;
			}
			if (a>45000) {
				a=45000;
			}
			y_val[0]=String.valueOf(a);
			if (a>32767) {
				y_val[1]="32767";
				y_val[2]=String.valueOf(a-32767);
			}                               
			else if (a<32767) {
				y_val[1]=y_val[0];
				y_val[2]="0";
			}
			return y_val;
		}
		
		// find cross product
		public static double[] cros(double ax, double ay, double az,
				double bx, double by, double bz) {
			double plane[] = new double[3];
			
			double cross_i1=(ay*bz);
			double cross_i2=(az*by);
			double cross_i=cross_i1-cross_i2;
			double cross_j1=(az*bx);
			double cross_j2=(ax*bz);
			double cross_j=cross_j1-cross_j2;
			double cross_k1=(ax*by);
			double cross_k2=(ay*bx);
			double cross_k=cross_k1-cross_k2;

			plane[0]=cross_i;
			plane[1]=cross_j;
			plane[2]=cross_k;
			
			return plane;
		};
			
		// main menu bar
		public void menubar() {										
		JMenuBar bar=new JMenuBar();

		JMenu help= new JMenu("Help");											
		help.setMnemonic(KeyEvent.VK_F);//set mnemonic key F
		help.setCursor(cusor);    

		JMenuItem manual=new JMenuItem("Manual");
		manual.setMnemonic(KeyEvent.VK_E);//set mnemonic key E
		manual.setCursor(cusor);
		manual.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				JOptionPane.showMessageDialog(null, "Manual");
			}
		}); 

		help.add(manual);
		bar.add(help);

		setJMenuBar(bar);
	}   

	//calibration
	public void calibration(String move, String val_1, String val_2, 
			String val_3, String val_4, String val_5) {
		try { //....................................................................................edited line ....................................................................................
			
			Runtime.getRuntime().exec("python "+dire+"/calibration.py"
					+" "+move+" "+val_1+" "+val_2+" "+val_3+" "+val_4+" "+val_5);
		}
		catch (IOException e1) {
			e1.printStackTrace();
		}
	}

	
	public void process_stat(JButton but_1, JButton but_2, String stat) {
		but_1.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				Runnable runner = new Runnable() {
					public void run() {
						but_1.setEnabled(false);
						but_2.setEnabled(true);
						try {//..........................................................................edited line..............................................................................
							
							Runtime.getRuntime().exec("python "+dire+"/sta.py "+stat);
						}
						catch (IOException e) {
							e.printStackTrace();
						}
					}
				};
				Thread t=new Thread(runner);
				t.start();    
			}
		});
	}
	
	// Access Camera functionality 
	
	public void camera_fiducials(String camval_1, String camval_2, String camval_3, String camval_4, String camval_5, String camval_6, String x_offset_val, String y_offset_val ) {
						try {
							
							Runtime.getRuntime().exec("python "+dire+"/fiducials_camera.py"
							+" "+camval_1+" "+camval_2+" "+camval_3+" "+camval_4+" "+camval_5+" "+camval_6+" "+x_offset_val+" "+y_offset_val);
						}
						catch (IOException e) {
							e.printStackTrace();
						}
					}
	public void overwatch() {
		try {
			
			Runtime.getRuntime().exec("python "+dire+"/online.py");
		}
		catch (IOException e) {
			e.printStackTrace();
		}
	}
				
	public void closeCamera() {
		try {
			
			Runtime.getRuntime().exec("python "+dire+"/closecamera.py");
		}
		catch (IOException e) {
			e.printStackTrace();
		}
	}	

	public ComboBoxes() {
		//drop down menu
		Container cp=getContentPane();
		cp.setLayout(null);
		
		String []choices={"Spike Check tool setup","Calibration","Spike Check Process"};

		cb=new JComboBox(choices);
		cb.setCursor(cusor);
		cb.setBounds(100,50,170,30);
		cb.setFont(new Font("Calibri", Font.PLAIN, 14));
	
		JButton btn = new JButton("OK");
		btn.setCursor(cusor);
		btn.setBounds(300,50,100,30);

		btn.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				lab.setText(String.valueOf(cb.getSelectedItem()));

					// SPIKE CHECK TOOL SETUP
				if (cb.getSelectedIndex()==0) {  
					//open new dialogue box
					dia=new JDialog();
					dia.setVisible(true);
					dia.setLocationRelativeTo(cp);
					dia.setTitle("Spike Check Tool Setup");
					dia.setSize(900,600);
					close(dia);

					Font myFont = new Font("Calibri", Font.BOLD, 13);
					
					String text_1 = "Step 1" + "<br>" + 
							"Load test flow using SmarTest" + "<br>" + "<br>";
					JLabel tex_1 = new JLabel("<html><div style='text-align: center;'>" + 
							text_1 + "</div></html>");

					String text_2 = "Step 2" + "<br>" + 
							"Input pins'information" + "<br>" + 
							"Sort according to pin from schematic" + "<br>"+ "<br>";
					JLabel tex_2 = new JLabel("<html><div style='text-align:"
							+ " center;'>" + 
							text_2 + "</div></html>");

					String text_3 = "Step 3" + "<br>" + 
							"Choose directory that report is saved to"+ "<br>" + "<br>";
					JLabel tex_3 = new JLabel("<html><div style='text-align: center;'>" + 
							text_3 + "</div></html>");

					String text_4= "Step 4" + "<br>" +
							"Choose Oscilloscope model" + "<br>" + "<br>";
					JLabel tex_4=new JLabel("<html><div style='text-align: center;'>" + 
							text_4 + "</div></html>");

					String text_5= "Step 5" + "<br>" +
							"Choose Oscilloscope connection mode" + "<br>" + "<br>";
					JLabel tex_5=new JLabel("<html><div style='text-align: center;'>" + 
							text_5 + "</div></html>");

					String text_6= "Step 6" + "<br>" +
							"Enter Oscilloscope IP address" + "<br>" + "<br>";
					JLabel tex_6=new JLabel("<html><div style='text-align: center;'>" + 
							text_6 + "</div></html>");

					String text_7= "Step 7" + "<br>" +
							"Enter Oscilloscope port" + "<br>" + "<br>";
					JLabel tex_7=new JLabel("<html><div style='text-align: center;'>" + 
							text_7 + "</div></html>");

					String text_8= "Step 8" + "<br>" +
							"Enter Oscilloscope channel number" + "<br>" + "<br>";
					JLabel tex_8=new JLabel("<html><div style='text-align: center;'>" + 
							text_8 + "</div></html>");

					JLabel tex_2c=new JLabel("No information file");                    
					JLabel tex_3c=new JLabel("No directory chosen");                    
					JLabel tex_4c=new JLabel("No model chosen ");                    
					JLabel tex_5c=new JLabel("No connection type chosen");                    
					JLabel tex_6c=new JLabel("No IP address entered");                    
					JLabel tex_7c=new JLabel("No port entered");                    
					JLabel tex_8c=new JLabel("No channel number entered");

					tex_1.setFont(myFont);
					tex_2.setFont(myFont);
					tex_3.setFont(myFont);
					tex_4.setFont(myFont);
					tex_5.setFont(myFont);
					tex_6.setFont(myFont);
					tex_7.setFont(myFont);
					tex_8.setFont(myFont);
					
					tex_1.setPreferredSize(new Dimension(250,50));
					tex_2.setPreferredSize(new Dimension(250,120));
					tex_5.setPreferredSize(new Dimension(250,120));
					tex_6.setPreferredSize(new Dimension(250,120));
					tex_7.setPreferredSize(new Dimension(250,120));
					tex_8.setPreferredSize(new Dimension(250,120));
					
					JButton but_1 = new JButton("Input");
					but_1.setCursor(cusor);

					JButton but_2 = new JButton("Choose directory");
					but_2.setCursor(cusor);

					JButton but_3 = new JButton("Save all values");
					but_3.setCursor(cusor);

					//oscilloscope model
					String []box_opt_1={"m1: Agilent infiniium 54830 Series",
							"m2: Agilent infiniium 3000 Series",
							"m3: Agilent infiniium 4000 Series",
							"m4: Agilent infiniium 6000 Series",
					"m5: Tektronix TDS 3024B Series"};      
					JComboBox box_1=new JComboBox(box_opt_1);
					box_1.setCursor(cusor);

					//oscilloscope connection mode
					String []box_opt_2={"USB","GPIB"}; 
					JComboBox box_2=new JComboBox(box_opt_2);
					box_2.setCursor(cusor);

					//oscilloscope IP address
					MaskFormatter mf = null;
					try {
						mf = new MaskFormatter("###.###.###.###");
					} 
					catch (java.text.ParseException e1) {
						e1.printStackTrace(); 
					}
					JFormattedTextField textfield_1 = new JFormattedTextField(mf);
					textfield_1.setColumns(9);

					JTextField textfield_2 = new JTextField(9);

					JTextField textfield_3 = new JTextField(3);

					//input button
					but_1.addActionListener(new ActionListener() {		
						@Override
						public void actionPerformed(ActionEvent e) {
							Runnable runner = new Runnable() {
								public void run() {
									try {    
										Runtime.getRuntime().exec("rundll32 url.dll,FileProtocolHandler "
												+ dire+"/pin_info.xlsm");
										tex_2c.setText("Input pins' information");
									}
									catch (IOException e1) {
										e1.printStackTrace();
										tex_2c.setText("Error");
									}
								}
							};
							Thread t=new Thread(runner);
							t.start();
						}
					});             

					//choose directory button
					but_2.addActionListener(new ActionListener() {		
						@Override
						public void actionPerformed(ActionEvent e) {
							Runnable runner = new Runnable() {
								public void run() {
									JFileChooser dircho=new JFileChooser(FileSystemView.getFileSystemView().
											getHomeDirectory());
									dircho.setDialogTitle("Choose directory");
									dircho.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);

									int retVal=dircho.showSaveDialog(null);
									if (retVal==JFileChooser.APPROVE_OPTION) {
										if (dircho.getSelectedFile().isDirectory()) {
											dir_out=dircho.getSelectedFile().toString();
											tex_3c.setText(dir_out);
										}
									}
								}
							};
							Thread t=new Thread(runner);
							t.start();           
						}
					});             

					//save all values button
					but_3.addActionListener(new ActionListener() {		
						@Override
						public void actionPerformed(ActionEvent e) {
							BufferedWriter writer;
							try {
								Runtime.getRuntime().exec("python "+dire+"/pin_info.py");
								if ((tex_3c.getText()=="No directory chosen") ||
										(tex_4c.getText()=="No model chosen") ||
										(tex_5c.getText()=="No connection type chosen") ||
										(tex_6c.getText()=="No IP address entered") ||
										(tex_7c.getText()=="No port entered") ||
										(tex_8c.getText()=="No channel number entered") ||
										(tex_8c.getText()=="Invalid number") ||
										(tex_8c.getText()=="Invalid value")) {
									JOptionPane.showMessageDialog(null, "Scope setup not finished");
								}
								else {
									String scope=tex_3c.getText()+" "+tex_4c.getText()+" "+tex_5c.getText()
									+" "+tex_6c.getText()+" "+tex_7c.getText()+" "+tex_8c.getText();
									writer = new BufferedWriter(new FileWriter(dire+"/scope_info.txt"));
									writer.write(scope);
									writer.close();
								}                                                              
							} 
							catch (IOException e1) {
								e1.printStackTrace();
							}
						}
					});

					box_1.addActionListener(new ActionListener() {		//	Agilent
						@Override
						public void actionPerformed(ActionEvent e) {
							tex_4c.setText(String.valueOf(box_1.getSelectedItem()));
						}
					});

					box_2.addActionListener(new ActionListener() {		//	USB
						@Override
						public void actionPerformed(ActionEvent e) {
							tex_5c.setText(String.valueOf(box_2.getSelectedItem()));
						}
					});

					textfield_1.addActionListener(new ActionListener() {	
						@Override
						public void actionPerformed(ActionEvent e) {
							tex_6c.setText(textfield_1.getText());
						}
					});

					textfield_2.addActionListener(new ActionListener() {	
						@Override
						public void actionPerformed(ActionEvent e) {
							tex_7c.setText(textfield_2.getText());
						}
					});

					textfield_3.addActionListener(new ActionListener() {
						@Override
						public void actionPerformed(ActionEvent e) {
							try {
								if (Integer.valueOf(textfield_3.getText())<0) {
									tex_8c.setText("Invalid number");
								}
								else {
									tex_8c.setText(textfield_3.getText());
								}
							}
							catch (NumberFormatException ex) {
								tex_8c.setText("Invalid value");   
							}
						}
					});

					JPanel butpan=new JPanel();
					butpan.add(tex_1);
					butpan.add(tex_2);
					butpan.add(but_1);
					butpan.add(tex_2c);
					butpan.add(tex_3);
					butpan.add(but_2);
					butpan.add(tex_3c);
					butpan.add(box_1);
					butpan.add(tex_4);
					butpan.add(tex_4c);
					butpan.add(box_2);
					butpan.add(tex_5);
					butpan.add(tex_5c);
					butpan.add(tex_6);
					butpan.add(tex_6c);
					butpan.add(textfield_1);
					butpan.add(tex_7);
					butpan.add(tex_7c);
					butpan.add(textfield_2);
					butpan.add(tex_8);
					butpan.add(tex_8c);
					butpan.add(textfield_3);
					butpan.add(but_3);
					butpan.setLayout(null); 
					set_position(butpan, tex_1, 35, 10);
					set_position(butpan, tex_2, 15, 45);
					set_position(butpan, but_1, 350, 85);
					set_position(butpan, tex_2c, 600, 85);
					set_position(butpan, tex_3, 6, 140);
					set_position(butpan, but_2, 350, 150);
					set_position(butpan, tex_3c, 600, 150);
					set_position(butpan, tex_4, 39, 205);
					set_position(butpan, box_1, 350, 220);
					set_position(butpan, tex_4c, 600, 220);
					set_position(butpan, tex_5, 10, 230);
					set_position(butpan, box_2, 350, 280);
					set_position(butpan, tex_5c, 600, 280);
					set_position(butpan, tex_6, 35, 280);
					set_position(butpan, textfield_1, 350, 330);
					set_position(butpan, tex_6c, 600, 330);
					set_position(butpan, tex_7, 50, 340);
					set_position(butpan, textfield_2, 350, 390);
					set_position(butpan, tex_7c, 600, 390);
					set_position(butpan, tex_8, 15, 400);
					set_position(butpan, textfield_3, 350, 450);
					set_position(butpan, tex_8c, 600, 450);
					set_position(butpan, but_3, 350, 490);

					dia.add(butpan,BorderLayout.CENTER);
				}               

			// CALIBRATION
				else if (cb.getSelectedIndex()==1) {

					ArrayList <Integer> x_tilt = new ArrayList<Integer>();
					ArrayList <Integer> y_tilt = new ArrayList<Integer>();
					ArrayList <Integer> z_tilt = new ArrayList<Integer>();
					
					for (int i=0; i <3; i++) {
						x_tilt.add(0);
						y_tilt.add(0);
						z_tilt.add(0);
					}

					dia=new JDialog();
					dia.setVisible(true);
					dia.setLocationRelativeTo(cp);
					dia.setSize(900, 800);
					dia.setFont(new Font("Calibri", Font.PLAIN, 12));
					close(dia);

					fid_cal=0;

					JLabel tex=new JLabel("Calibration according to 3 fiducials");

					String text_1 = "Step 1" + "<br>" + 
							"Choose file contaning all pins coordinates" + "<br>" + 
							"(Usually in form of \"place_txt.txt\")" + "<br>"+ "<br>";
					JLabel tex_1 = new JLabel("<html><div style='text-align: center;'>" + 
							text_1 + "</div></html>");

					String text_2 = "<br>"+"Step 2" + "<br>" + 
							"Calibrate the marked fiducial below" + "<br>" + "<br>";
					JLabel tex_2 = new JLabel("<html><div style='text-align: center;'>" + 
							text_2 + "</div></html>");

					JLabel tex_1c=new JLabel("No file chosen");

					tex_1.setPreferredSize(new Dimension(170,130));

					
					JLabel X_label = new JLabel("X-AXIS");
					JLabel Y_label = new JLabel("Y-AXIS");
					JLabel Z_label = new JLabel("Z-AXIS");

					BasicArrowButton X_left_coarse = new BasicArrowButton(BasicArrowButton.WEST);
					BasicArrowButton X_right_coarse = new BasicArrowButton(BasicArrowButton.EAST);
					BasicArrowButton X_left_medium = new BasicArrowButton(BasicArrowButton.WEST);
					BasicArrowButton X_right_medium = new BasicArrowButton(BasicArrowButton.EAST);
					BasicArrowButton X_left_fine = new BasicArrowButton(BasicArrowButton.WEST);
					BasicArrowButton X_right_fine = new BasicArrowButton(BasicArrowButton.EAST);
					BasicArrowButton Y_left_coarse = new BasicArrowButton(BasicArrowButton.WEST);
					BasicArrowButton Y_right_coarse = new BasicArrowButton(BasicArrowButton.EAST);
					BasicArrowButton Y_left_medium = new BasicArrowButton(BasicArrowButton.WEST);
					BasicArrowButton Y_right_medium = new BasicArrowButton(BasicArrowButton.EAST);
					BasicArrowButton Y_left_fine = new BasicArrowButton(BasicArrowButton.WEST);
					BasicArrowButton Y_right_fine = new BasicArrowButton(BasicArrowButton.EAST);
					BasicArrowButton Z_up = new BasicArrowButton(BasicArrowButton.NORTH);
					BasicArrowButton Z_down = new BasicArrowButton(BasicArrowButton.SOUTH);

					JTextField X_value= new JTextField("0",9);
					JTextField Y_value= new JTextField("0",9);
					JTextField Z_value= new JTextField("0",9);
					
					JSlider X_slider = new JSlider(JSlider.HORIZONTAL, 1, 500, 1);                 
					JSlider Y_slider = new JSlider(JSlider.HORIZONTAL, 1, 500, 1);                 
					JSlider Z_slider = new JSlider(JSlider.HORIZONTAL, 1, 500, 1);

					Hashtable<Integer, JLabel> labelTable = new Hashtable<Integer, JLabel>();
					labelTable.put(new Integer(1), new JLabel("1") );
					labelTable.put(new Integer(100), new JLabel("100") );
					labelTable.put(new Integer(500), new JLabel("500") );

					X_slider.setLabelTable(labelTable);
					X_slider.setPaintLabels(true);
					X_slider.setMajorTickSpacing(100);
					X_slider.setPaintTicks(true);

					Y_slider.setLabelTable(labelTable);
					Y_slider.setPaintLabels(true);
					Y_slider.setMajorTickSpacing(100);
					Y_slider.setPaintTicks(true);

					Z_slider.setLabelTable(labelTable);
					Z_slider.setPaintLabels(true);
					Z_slider.setMajorTickSpacing(100);
					Z_slider.setPaintTicks(true);                                                  

					JButton but_1 = new JButton("Choose file");
					but_1.setCursor(cusor);
					but_1.setPreferredSize(new Dimension(100,25));
					
					JButton but_2 = new JButton("Move");
					but_2.setCursor(cusor);
					but_2.setPreferredSize(new Dimension(100,25));
					
					JButton but_3 = new JButton("Done");
					but_3.setCursor(cusor);
					but_3.setEnabled(true);
					but_3.setPreferredSize(new Dimension(100,25));
					
					JButton but_4 = new JButton("Finish Calibration");
					but_4.setCursor(cusor);
					but_4.setEnabled(false);
					but_4.setPreferredSize(new Dimension(150,30));
					
					JButton but_5 = new JButton("Use Joystick");
					but_5.setCursor(cusor);
					but_5.setEnabled(true);

					JButton but_6 = new JButton("Offset Calibration");
					but_6.setCursor(cusor);
					but_6.setEnabled(true);
					but_6.setPreferredSize(new Dimension(150,30));
					
					//image in interface
					ImageIcon image = new ImageIcon(dire+"/GUI.png");
					JLabel ima_lab = new JLabel("", image, JLabel.CENTER);

					JLabel lab_1 = new JLabel("Coarse [50 mm]");
					JLabel lab_2 = new JLabel("Medium [20 mm]");
					JLabel lab_3 = new JLabel("Fine");                    
					JLabel lab_4 = new JLabel("Position [0.01 mm]");
					JLabel lab_5 = new JLabel("Amount of distance changed [0.01 mm]");
					JLabel lab_6 = new JLabel(fid_cal+" fiducial(s)");
					
					//points in the image
					JLabel point1 = new JLabel("Point 1                                             ");
					JLabel point2 = new JLabel("Point 2                                             ");
					JLabel point3 = new JLabel("Point 3                                             ");

					point1.setEnabled(false);
					point2.setEnabled(false);
					point3.setEnabled(false);

					X_left_coarse.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							x_change=Integer.valueOf(X_value.getText())-5000;
							x_val=check_x(x_change);
							X_value.setText(x_val[0]);
							calibration("X_value", x_val[1], x_val[2], x_val[3], "0", "0");
						}
					});

					X_right_coarse.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							x_change=Integer.valueOf(X_value.getText())+5000;
							x_val=check_x(x_change);
							X_value.setText(x_val[0]);
							calibration("X_value", x_val[1], x_val[2], x_val[3], "0", "0");
						}
					});

					X_left_medium.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							x_change=Integer.valueOf(X_value.getText())-2000;
							x_val=check_x(x_change);
							X_value.setText(x_val[0]);   
							calibration("X_value", x_val[1], x_val[2], x_val[3], "0", "0");
						}
					});

					X_right_medium.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							x_change=Integer.valueOf(X_value.getText())+2000;
							x_val=check_x(x_change);
							X_value.setText(x_val[0]);
							calibration("X_value", x_val[1], x_val[2], x_val[3], "0", "0");
						}
					});

					X_left_fine.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							x_change=Integer.valueOf(X_value.getText())-X_slider.getValue();
							x_val=check_x(x_change);
							X_value.setText(x_val[0]);
							calibration("X_value", x_val[1], x_val[2], x_val[3], "0", "0");
						}
					});

					X_right_fine.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							x_change=Integer.valueOf(X_value.getText())+X_slider.getValue();
							x_val=check_x(x_change);
							X_value.setText(x_val[0]);
							calibration("X_value", x_val[1], x_val[2], x_val[3], "0", "0");
						}
					});

					Y_left_coarse.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							y_change=Integer.valueOf(Y_value.getText())-5000;
							y_val=check_y(y_change);
							Y_value.setText(y_val[0]);
							calibration("Y_value", y_val[1], y_val[2], "0", "0", "0");
						}
					});

					Y_right_coarse.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							y_change=Integer.valueOf(Y_value.getText())+5000;
							y_val=check_y(y_change);
							Y_value.setText(y_val[0]);
							calibration("Y_value", y_val[1], y_val[2], "0", "0", "0");
						}
					});

					Y_left_medium.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							y_change=Integer.valueOf(Y_value.getText())-2000;
							y_val=check_y(y_change);
							Y_value.setText(y_val[0]);
							calibration("Y_value", y_val[1], y_val[2], "0", "0", "0");   
						}
					});

					Y_right_medium.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							y_change=Integer.valueOf(Y_value.getText())+2000;
							y_val=check_y(y_change);
							Y_value.setText(y_val[0]);
							calibration("Y_value", y_val[1], y_val[2], "0", "0", "0");
						}
					});

					Y_left_fine.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							y_change=Integer.valueOf(Y_value.getText())-Y_slider.getValue();
							y_val=check_y(y_change);
							Y_value.setText(y_val[0]);
							calibration("Y_value", y_val[1], y_val[2], "0", "0", "0");
						}
					});

					Y_right_fine.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							y_change=Integer.valueOf(Y_value.getText())+Y_slider.getValue();
							y_val=check_y(y_change);
							Y_value.setText(y_val[0]);
							calibration("Y_value", y_val[1], y_val[2], "0", "0", "0");
						}
					});

					Z_up.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							z_change=Integer.valueOf(Z_value.getText())-Z_slider.getValue();
							if (z_change<0) {
								z_change=0;
							}
							Z_value.setText(String.valueOf(z_change));
							calibration("Z_value", String.valueOf(z_change), "0", "0", "0", "0");
						}
					});

					Z_down.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							z_change=Integer.valueOf(Z_value.getText())+Z_slider.getValue();
							if (z_change>10000) {
								z_change=10000;
							}
							Z_value.setText(String.valueOf(z_change));
							calibration("Z_value", String.valueOf(z_change), "0", "0", "0", "0");
						}
					});

					X_value.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							try {
								String data=X_value.getText();
								if (Integer.valueOf(data)>=0 && Integer.valueOf(data)<=75000) {
									x_val=check_x(Integer.valueOf(data));
									
									calibration("X_value", x_val[1], x_val[2], x_val[3], "0", "0");
								}
								else {
									JOptionPane.showMessageDialog(null, "Invalid value for X travel");
								}
								
							}
							catch (NumberFormatException ex) {
								JOptionPane.showMessageDialog(null, "Not a number");
							}
						}
					});

					Y_value.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							try {
								String data=Y_value.getText();
								if (Integer.valueOf(data)>=0 && Integer.valueOf(data)<=45000) {
									y_val=check_y(Integer.valueOf(data));
									
									calibration("Y_value", y_val[1], y_val[2], "0", "0", "0");
								}
								else {
									JOptionPane.showMessageDialog(null, "Invalid value for Y travel");
								}
								
							}
							catch (NumberFormatException ex) {
								JOptionPane.showMessageDialog(null, "Not a number");
							}
						}
					});

					Z_value.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							try {
								String data=Z_value.getText();
								if (Integer.valueOf(data)>=0 && Integer.valueOf(data)<=10000) {
								
									calibration("Z_value", data, "0", "0", "0", "0");
								}
								
								else {
									JOptionPane.showMessageDialog(null, "Invalid value for Z travel");
								}
								
							}
							catch (NumberFormatException ex) {
								JOptionPane.showMessageDialog(null, "Not a number");
							}
						}
						
					});
					
					//Joy stick  
					but_5.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {  
							Runnable runner = new Runnable() {public void run() {
								
								but_5.setForeground(Color.red);
								
								//choose port which will always be associated to COM3
								try {
								SerialPort ports = SerialPort.getCommPorts()[0];
								
								// SerialPort.getCommPorts()[0] will only have COM3 as the accessible port
								
								SerialPort serialPort = ports;
								if(serialPort.openPort())
									System.out.println("Port opened successfully.");
								else {
									System.out.println("Unable to open the port.");
									return;
								}
								
								
								// ComPortParameters(Baud, Data bits,StopBits, Parity);
								
								serialPort.setComPortParameters(9600, 8, 1, SerialPort.NO_PARITY);
								serialPort.setComPortTimeouts(SerialPort.TIMEOUT_SCANNER, 0, 0);

								BufferedReader data = new BufferedReader(new InputStreamReader(serialPort.getInputStream()));
								String dataL;
								//continuous loop to receive data
								
								
								while( (dataL = data.readLine() ) != null){
									//System.out.println(data.nextLine());
							try {
								// Adds to the Values in the TextFields on each loop
								
									int x_initial=Integer.valueOf(X_value.getText());
									int y_initial=Integer.valueOf(Y_value.getText());
									int z_initial=Integer.valueOf(Z_value.getText());
									
									//X Axis
									System.out.println("Stage 1");
								    if(dataL.contains("X:")){
								    	System.out.println("Stage 2");
								    	but_5.setEnabled(false);
								    	but_5.setForeground(Color.red);
								    	//Change background of X_Value
								    	X_value.setBackground(Color.orange);
										Y_value.setBackground(Color.white);
										Z_value.setBackground(Color.white);
										// assign x value to a variable
								    	String x = null;
										try {
											x = data.readLine();
										} catch (IOException e) {
											// TODO Auto-generated catch block
											e.printStackTrace();
										}
								    	// convert x value from string to integer
										System.out.println("Stage 3");
								    	int X= Integer.parseInt(x);
								    	x_change=x_initial+X;
								    	x_val=check_x(x_change);
								    	X_value.setText(x_val[0]);
								    	calibration("X_value", x_val[1], x_val[2], x_val[3], "0", "0");
								    }
								    
								    //Y Axis
								    
								    if(dataL.contains("Y:")){
								    	System.out.println("Stage 2");
								    	but_5.setEnabled(false);
								    	but_5.setForeground(Color.red);
								    	Y_value.setBackground(Color.orange);
										X_value.setBackground(Color.white);
										Z_value.setBackground(Color.white);
									      // y value
								    	String y = null;
										try {
											y = data.readLine();
										} catch (IOException e) {
											// TODO Auto-generated catch block
											e.printStackTrace();
										}
										System.out.println("Stage 3");
										System.out.println(y);
										String[] parts = y.split(": ");
										String part1 = parts[0]; // Y
										String part2 = parts[1]; // Integer Value
								    	//convert y value from string to integer
										System.out.println(part2);
										int Y= Integer.parseInt(part2);
										System.out.println("Stage 4");
								    	y_change=y_initial+Y;
								    	System.out.println("Stage 5");
										y_val=check_y(y_change);
										Y_value.setText(y_val[0]);
										calibration("Y_value", y_val[1], y_val[2], "0", "0", "0");
									    }
								    
								    // Z Axis
								    
								    if(dataL.contains("Z:")){
								    	but_5.setEnabled(false);
								    	but_5.setForeground(Color.red);
								    	Z_value.setBackground(Color.orange);
										Y_value.setBackground(Color.white);
										X_value.setBackground(Color.white);
									    // z value
								    	String z = null;
										try {
											z = data.readLine();
										} catch (IOException e) {
											// TODO Auto-generated catch block
											e.printStackTrace();
										}
								    	// convert z value from string to integer
										int Z= Integer.parseInt(z);
										z_change=z_initial+Z;
										if (z_change<0) {
											z_change=0;
										}
										Z_value.setText(String.valueOf(z_change));
										calibration("Z_value", String.valueOf(z_change), "0", "0", "0", "0");
									    }
								    if(dataL.contains("Double:")){
								    	
								    	 try {
											System.out.println("" + data.readLine());
										} catch (IOException e) {
											// TODO Auto-generated catch block
											e.printStackTrace();
										}
								    	 System.out.println("X:" +x_change+ " Y:" +y_change+ " Z:" +z_change);
								    }
								    if(dataL.contains("OFF")){
								    	
								    	try {
											data.close();
										} catch (IOException e) {
											// TODO Auto-generated catch block
											e.printStackTrace();
										}
								    	Z_value.setBackground(Color.white);
										Y_value.setBackground(Color.white);
										X_value.setBackground(Color.white);
								    	but_5.setEnabled(true);
								    	but_5.setForeground(Color.black);
								    	break;
								    }
								    
								}catch(NumberFormatException f) {
								System.out.println("Text box is Empty");
							}
								}
								
								System.out.println("Done.");
								serialPort.closePort();
								}catch(ArrayIndexOutOfBoundsException | IOException g) {
									JOptionPane.showMessageDialog(null, "Joystick is not connected.");	
									but_5.setEnabled(true);
									but_5.setForeground(Color.black);
								}	
							}
							
				};
				
				but_5.setEnabled(false);
				Thread t=new Thread(runner);
				t.start();
			
			}
			
		});            

					//"Choose file" button
					but_1.addActionListener(new ActionListener() {
						@Override
						public void actionPerformed(ActionEvent e) {
							Runnable runner = new Runnable() {
								public void run() {
									fid_cal=0;
									lab_6.setText(fid_cal+" fiducial(s)");
									//enable button
									but_3.setEnabled(true);
									//chose file
									JFileChooser ficho=new JFileChooser();
									ficho.setDialogTitle("Choose file");

									int retVal=ficho.showOpenDialog(null);
									if (retVal==JFileChooser.APPROVE_OPTION) {
										File selectedFile=ficho.getSelectedFile();
										//execute position.py file
										try {
											Runtime.getRuntime().exec("python "+dire+"/position.py"
													+ " "+selectedFile.getAbsolutePath()); 
										}
										catch (IOException e1) {
											e1.printStackTrace();
											JOptionPane.showConfirmDialog(null, "Please select a valid Position File!",
													"File maybe of the wrong format or does not have any data.",JOptionPane.CLOSED_OPTION);
										}
										tex_1c.setText(selectedFile.getAbsolutePath());

										try {
											TimeUnit.SECONDS.sleep(1);
										} catch (InterruptedException e1) {
											e1.printStackTrace();
										}

										try {
											File file = new File(dire+"/fiducial.txt");
											FileReader fileReader = new FileReader(file);
											BufferedReader bufferedReader = new BufferedReader(fileReader);
											StringBuffer stringBuffer = new StringBuffer();
											String line;
											while ((line = bufferedReader.readLine()) != null) {
												stringBuffer.append(line);
												stringBuffer.append("\n");
											}
											fileReader.close();
											String fid=stringBuffer.toString();
											String lines[] = fid.split("\\r?\\n");                                          

											JCheckBox fiducials[] = new JCheckBox[lines.length];

											for(int i=0; i<lines.length; i++)
											{
												fiducials[i] = new JCheckBox(lines[i]);
											}

											String msg = "Choose fiducials visible on the PCB"; 

											Object[] msgContent = {msg, fiducials}; 

											int n = JOptionPane.showConfirmDialog (dia,  msgContent,  "Fiducials", JOptionPane.OK_CANCEL_OPTION); 

											if (n==0) {
												ArrayList<String> vis_fid = new ArrayList<String>();
												for (int i=0; i<lines.length; i++) {
													if (fiducials[i].isSelected()) {
														vis_fid.add(String.valueOf(fiducials[i].getText()));
													}
												}
												System.out.println(vis_fid);

												float x_1=0;
												float x_2=0;
												float x_3=0;
												float y_1=0;
												float y_2=0;
												float y_3=0;
												int i_1=0;
												int i_2=0;
												int i_3=0;
												for (int i=0; i<vis_fid.size(); i++) {
													String[] val = String.valueOf(vis_fid.get(i)).split("\\s+");
													if ((x_1 >= Float.valueOf(val[1])) && (y_1 <= Float.valueOf(val[2]))){
														x_1= Float.valueOf(val[1]);
														y_1=Float.valueOf(val[2]);
														i_1=i;
													}
													if ((x_2 >= Float.valueOf(val[1])) && (y_2 >= Float.valueOf(val[2]))) {
														x_2= Float.valueOf(val[1]);
														y_2=Float.valueOf(val[2]);
														i_2=i;
													}
													if ((x_3 <= Float.valueOf(val[1])) && (y_3 >= Float.valueOf(val[2]))) {
														x_3=Float.valueOf(val[1]);
														y_3=Float.valueOf(val[2]);
														i_3=i;
													}
												}
												point1.setText(String.valueOf(vis_fid.get(i_1)));
												point2.setText(String.valueOf(vis_fid.get(i_2)));
												point3.setText(String.valueOf(vis_fid.get(i_3)));

												point1.setEnabled(true);
												point1.setForeground(Color.red);
												point2.setEnabled(false);
												point3.setEnabled(false);
												ImageIcon image = new ImageIcon(dire+"/GUI_1.png");
												ima_lab.setIcon(image);

											}

										} catch (IOException e) {
											
											JOptionPane.showConfirmDialog(null, "Wrong File Selected!","Check Name / Format of File.",JOptionPane.CLOSED_OPTION);
	
											e.printStackTrace();
										}
									
									}
									else {
										tex_1c.setText("No file chosen");
									}
								}
							};
							Thread t=new Thread(runner);
							t.start();
						}
					});             

					//"Move" button
					but_2.addActionListener(new ActionListener() {
						@Override
						public void actionPerformed(ActionEvent e) {
							Runnable runner = new Runnable() {
								public void run() {
									if (point1.getText().contains("Point") || point2.getText().contains("Point") || point3.getText().contains("Point")) {
										JOptionPane.showConfirmDialog(null, "No fiducials chosen, redo Step 1!","Fiducials input error",JOptionPane.CLOSED_OPTION);
									}
									else if (point1.getText().equals(point2.getText()) || point2.getText().equals(point3.getText()) || 
											point1.getText().equals(point3.getText())) {
										JOptionPane.showConfirmDialog(null, "Not enough fiducials chosen, redo Step 1!",
												"Fiducials input error",JOptionPane.CLOSED_OPTION);
									}

									else {
										String[] off=null;
										String fid_s1=point1.getText();
										fid_1 = fid_s1.split("\\s+");
										String fid_s2=point2.getText();
										fid_2 = fid_s2.split("\\s+");
										String fid_s3=point3.getText();
										fid_3 = fid_s3.split("\\s+");

										try {
											File f = new File(dire+"/offset.txt");
											BufferedReader b = new BufferedReader(new FileReader(f));
											String offs = null;                                         
											while ((offs = b.readLine()) != null) {
												off = offs.split("\\s+");
												System.out.println("X_off: "+off[0]+", Y_off: "+off[1]);
											}
											b.close();
										}
										catch (IOException e1) {
											e1.printStackTrace();
										}

										if (fid_cal==0) {
											fid_x_1=Math.round(Float.valueOf(off[0]));
											fid_y_1=Math.round(Float.valueOf(off[1]));
											X_value.setText(String.valueOf(fid_x_1));
											Y_value.setText(String.valueOf(fid_y_1));
											x_val=check_x(fid_x_1);
											y_val=check_y(fid_y_1);
											System.out.println("Point1: "+fid_x_1+" "+fid_y_1);
										}
										if (fid_cal==1) {
											int x_dif=(int) (100*(Float.valueOf(fid_1[1])-Float.valueOf(fid_2[1])));
											int y_dif=(int) (100*(Float.valueOf(fid_1[2])-Float.valueOf(fid_2[2])));
											System.out.println("X_dif: "+x_dif+", Y_dif: "+y_dif);
											fid_x_2=x_tilt.get(0)-x_dif;
											fid_y_2=y_tilt.get(0)-y_dif;
											X_value.setText(String.valueOf(fid_x_2));
											Y_value.setText(String.valueOf(fid_y_2));
											x_val=check_x(fid_x_2);
											y_val=check_y(fid_y_2);
											System.out.println("Point2: "+fid_x_2+" "+fid_y_2);

										}
										if (fid_cal==2) {
											int x_dif=(int) (100*(Float.valueOf(fid_2[1])-Float.valueOf(fid_3[1])));
											int y_dif=(int) (100*(Float.valueOf(fid_2[2])-Float.valueOf(fid_3[2])));
											System.out.println("X_dif: "+x_dif+", Y_dif: "+y_dif);
											fid_x_3=x_tilt.get(1)-x_dif;
											fid_y_3=y_tilt.get(1)-y_dif;
											X_value.setText(String.valueOf(fid_x_3));
											Y_value.setText(String.valueOf(fid_y_3));
											x_val=check_x(fid_x_3);
											y_val=check_y(fid_y_3);
											System.out.println("Point3: "+fid_x_3+" "+fid_y_3);

										}
										calibration("Move", x_val[1], x_val[2], x_val[3], y_val[1], y_val[2]);
									}
								}
							};
							Thread t=new Thread(runner);
							t.start();
						}
					}); 
					
					
					// "Offset Calibration" Button
					but_6.addActionListener(new ActionListener() {
						@Override
						public void actionPerformed(ActionEvent e) {
							Runnable runner = new Runnable() {
								public void run() {
									
									//make sure Z-travel is zero
									Z_zero = 0;
									calibration("Z_value", String.valueOf(Z_zero), "0", "0", "0", "0");
									
									overwatch(); // Turn on video capture
									
									//Initialize the new dialog box
									dia.setAlwaysOnTop(false);
									offfid=new JDialog();
									offfid.setLocationRelativeTo(dia);
									offfid.setSize(700,550);
									
									
									// Add the needed components (X,Y,Z - text boxes and the Calculate Average Offset button)
									JLabel X_new = new JLabel("X-AXIS");
									JLabel Y_new = new JLabel("Y-AXIS");
									
									String exp_fid = "OFFSET CALIBRATION" + "<br>" + 
											"Enter the respective X and Y values till the camera is at the centre point of the Fiducial" + "<br>" + 
											"TIP : Wait for Image detection by the Camera for dead centre position " + "<br>"+ "<br>";
									JLabel exp_label = new JLabel("<html><div style='text-align: center;'>" + 
											exp_fid + "</div></html>");
									exp_label.setFont(new Font("Calibri", Font.BOLD, 14));
									
									JLabel avrgX = new JLabel("Average Offset:" +x_off); // Displays offsets for X 
									JLabel avrgY = new JLabel("Average Offset:" +y_off); // Displays offsets for Y 
									
									JTextField X_newval= new JTextField("0",9);
									JTextField Y_newval= new JTextField("0",9);
									
									JButton off_but = new JButton("Finish Offset Calibration");
								    off_but.setCursor(cusor);
								    off_but.setEnabled(true);
								    off_but.setPreferredSize(new Dimension(180,30));
								    
								    JButton close_cam = new JButton("Save Camera Position");
								    close_cam.setCursor(cusor);
								    close_cam.setEnabled(true);
								    
								    JButton joystick = new JButton("Use Joystick");
								    joystick.setCursor(cusor);
								    joystick.setEnabled(true);
								    
								    JButton position = new JButton("Move to Position");
								    position.setCursor(cusor);
								    position.setEnabled(true);
								    position.setPreferredSize(new Dimension(150,30));
								    
								    X_newval.setText(X_value.getText());
									Y_newval.setText(Y_value.getText());
									
									
								    X_newval.addActionListener(new ActionListener() {
										public void actionPerformed(ActionEvent e) {
											try {
												String vals=X_newval.getText();
												if (Integer.valueOf(vals)>=0 && Integer.valueOf(vals)<=75000) {
													x_val=check_x(Integer.valueOf(vals));
													
													calibration("X_value", x_val[1], x_val[2], x_val[3], "0", "0");
												}
												else {
													JOptionPane.showMessageDialog(null, "Invalid value for X travel");
												}
												
											}
											catch (NumberFormatException ex) {
												JOptionPane.showMessageDialog(null, "Not a number");
											}
										}
									});

									Y_newval.addActionListener(new ActionListener() {
										public void actionPerformed(ActionEvent e) {
											try {
												String vals=Y_newval.getText();
												if (Integer.valueOf(vals)>=0 && Integer.valueOf(vals)<=45000) {
													y_val=check_y(Integer.valueOf(vals));
													
													calibration("Y_value", y_val[1], y_val[2], "0", "0", "0");
												}
												else {
													JOptionPane.showMessageDialog(null, "Invalid value for Y travel");
												}
												
											}
											catch (NumberFormatException ex) {
												JOptionPane.showMessageDialog(null, "Not a number");
											}
										}
									});
									
									
									off_but.addActionListener(new ActionListener() {
										public void actionPerformed(ActionEvent e) {
											off_but.setEnabled(false);
											
											// counter
											i = i + 1;
											
											// Needed return position and new position
											
											x_orig =Integer.valueOf(X_value.getText());
											y_orig =Integer.valueOf(Y_value.getText());
											
											x_new =Integer.valueOf(X_newval.getText());
											y_new =Integer.valueOf(Y_newval.getText());
											
											// offsets
											
												x_off = (x_new - x_orig);
												y_off = (y_new - y_orig);
												
												/*
											}		
											if (i == 2) {
												x_off = (x_new - x_orig);
												y_off = (y_new - y_orig);
												
												
											}	
											if (i == 3) {
												x_off = (x_new - x_orig);
												y_off = (y_new - y_orig);
												
												*/
												
											
											
											x_val=check_x(x_orig);
											y_val=check_y(y_orig);
											
											// Set the x and y calibrations back to zero
											/*
											X_newval.setText(String.valueOf(0));
											Y_newval.setText(String.valueOf(0)); */
											
											
											X_value.setText(x_val[0]);
											calibration("X_value", x_val[1], x_val[2], x_val[3], "0", "0"); 
											
											
											avrgX.setText("Offset: " +(x_off)); 
											avrgY.setText("Offset: " +(y_off));
											
											
											 Timer t = new Timer(3000, null);
								                t.addActionListener(new ActionListener() {

								                    @Override
								                    public void actionPerformed(ActionEvent e) {
								                
								                        
								                        Y_value.setText(y_val[0]);
														calibration("Y_value", y_val[1], y_val[2], "0", "0", "0");
														
								                        offfid.dispose();

								                    }
								                });
								                t.setRepeats(false);
								                t.start();
										}
										
										
									});
									
									close_cam.addActionListener(new ActionListener() {
										public void actionPerformed(ActionEvent e) {
											
											Runnable runner = new Runnable() {
												public void run() {
													close_cam.setEnabled(false);
													try {//..........................................................................edited line..............................................................................
														
														/* Second method - Turning the camera off */
														 Runtime.getRuntime().exec("taskkill /F /IM python.exe");
									
													}
													catch (IOException e) {
														e.printStackTrace();
													}
												}
											};
											Thread t=new Thread(runner);
											t.start();  
										}});
									
	//.............................................Move to Last Fiducial Position...............................................................................................................		
									position.addActionListener(new ActionListener() {
										@Override
										public void actionPerformed(ActionEvent e) {
											Runnable runner = new Runnable() {
												public void run() {
													if (point1.getText().contains("Point") || point2.getText().contains("Point") || point3.getText().contains("Point")) {
														JOptionPane.showConfirmDialog(null, "No fiducials chosen, redo Step 1!","Fiducials input error",JOptionPane.CLOSED_OPTION);
													}
													else if (point1.getText().equals(point2.getText()) || point2.getText().equals(point3.getText()) || 
															point1.getText().equals(point3.getText())) {
														JOptionPane.showConfirmDialog(null, "Not enough fiducials chosen, redo Step 1!",
																"Fiducials input error",JOptionPane.CLOSED_OPTION);
													}

													else {
														//String[] off=null;
														String[] pos = null;
														String fid_s1=point1.getText();
														fid_1 = fid_s1.split("\\s+");
														String fid_s2=point2.getText();
														fid_2 = fid_s2.split("\\s+");
														String fid_s3=point3.getText();
														fid_3 = fid_s3.split("\\s+");

														try {
															File f = new File(dire+"/offsetposition.txt");
															BufferedReader b = new BufferedReader(new FileReader(f));
															String offs = null;                                         
															while ((offs = b.readLine()) != null) {
																pos = offs.split("\\s+");
																System.out.println("FD4: "+pos[0]+ ","+pos[1]+ " FD2: "+pos[2]+ ","+pos[3]+ " FD6: "+pos[4]+ ","+pos[5]);
															}
															b.close();
														}
														catch (IOException e1) {
															e1.printStackTrace();
														}

														if (fid_cal==0) {
															pos_x_1=Math.round(Float.valueOf(pos[0]));
															pos_y_1=Math.round(Float.valueOf(pos[1]));
															X_newval.setText(String.valueOf(pos_x_1));
															Y_newval.setText(String.valueOf(pos_y_1));
															x_val=check_x(pos_x_1);
															y_val=check_y(pos_y_1);
															System.out.println("FD4: "+pos_x_1+" "+pos_y_1);
														}
														if (fid_cal==1) {
															pos_x_2=Math.round(Float.valueOf(pos[2]));
															pos_y_2=Math.round(Float.valueOf(pos[3]));
															X_newval.setText(String.valueOf(pos_x_2));
															Y_newval.setText(String.valueOf(pos_y_2));
															x_val=check_x(pos_x_2);
															y_val=check_y(pos_y_2);
															System.out.println("FD2: "+pos_x_2+" "+pos_y_2);
														}
														if (fid_cal==2) {
															pos_x_3=Math.round(Float.valueOf(pos[4]));
															pos_y_3=Math.round(Float.valueOf(pos[5]));
															X_newval.setText(String.valueOf(pos_x_3));
															Y_newval.setText(String.valueOf(pos_y_3));
															x_val=check_x(pos_x_3);
															y_val=check_y(pos_y_3);
															System.out.println("FD6: "+pos_x_3+" "+pos_y_3);
														}
														calibration("Move", x_val[1], x_val[2], x_val[3], y_val[1], y_val[2]);
													}
												}
											};
											Thread t=new Thread(runner);
											t.start();
										}
									}); 
									
	//..........................................................................................................................................................................................								
									
									//Joy stick  
									joystick.addActionListener(new ActionListener() {
										public void actionPerformed(ActionEvent e) {  
											Runnable runner = new Runnable() {public void run() {
												
												joystick.setForeground(Color.red);
												
												X_newval.setText(X_value.getText());
												Y_newval.setText(Y_value.getText());
												
												//choose port which will always be associated to COM3
												try {
												SerialPort ports = SerialPort.getCommPorts()[0];
												
												// SerialPort.getCommPorts()[0] will only have COM3 as the accessible port
												
												SerialPort serialPort = ports;
												if(serialPort.openPort())
													System.out.println("Port opened successfully.");
												else {
													System.out.println("Unable to open the port.");
													return;
												}
												
												
												// ComPortParameters(Baud, Data bits,StopBits, Parity);
												
												serialPort.setComPortParameters(9600, 8, 1, SerialPort.NO_PARITY);
												serialPort.setComPortTimeouts(SerialPort.TIMEOUT_SCANNER, 0, 0);

												Scanner data = new Scanner(serialPort.getInputStream());
												
												//continuous loop to receive data
												
												while(data.hasNextLine()){
													//System.out.println(data.nextLine());
											try {
												// Adds to the Values in the TextFields on each loop
												
													int x_prev = Integer.valueOf(X_newval.getText()); 
													int y_prev = Integer.valueOf(Y_newval.getText()); 
													
													
													//X Axis
												    if(data.findInLine("X: ")!=null){
												    	joystick.setEnabled(false);
												    	joystick.setForeground(Color.red);
												    	//Change background of X_Value
												    	X_newval.setBackground(Color.orange);
														Y_newval.setBackground(Color.white);
														// assign x value to a variable
												    	String x= data.nextLine();
												    	// convert x value from string to integer
												    	int X= Integer.parseInt(x);
												    	x_diff =x_prev+X;
												    	x_val=check_x(x_diff);
												    	X_newval.setText(x_val[0]);
												    	calibration("X_value", x_val[1], x_val[2], x_val[3], "0", "0");
												    }
												    
												    //Y Axis
												    
												    if(data.findInLine("Y: ")!=null){
												    	joystick.setEnabled(false);
												    	joystick.setForeground(Color.red);
												    	Y_newval.setBackground(Color.orange);
														X_newval.setBackground(Color.white);
													      // y value
												    	String y= data.nextLine();
												    	//convert y value from string to integer
														int Y= Integer.parseInt(y);
												    	y_diff=y_prev+Y;
														y_val=check_y(y_diff);
														Y_newval.setText(y_val[0]);;
														calibration("Y_value", y_val[1], y_val[2], "0", "0", "0");
													    }
												    
												    //Z Axis
												    
												    if(data.findInLine("Z: ")!=null){
												    	joystick.setEnabled(false);
												    	joystick.setForeground(Color.red);
												    	//Change background of X_Value
												    	X_newval.setBackground(Color.orange);
														Y_newval.setBackground(Color.white);
														// assign x value to a variable
												    	String x= data.nextLine();
												    	// convert x value from string to integer
												    	int X= Integer.parseInt(x);
												    	x_diff=x_prev+X;
												    	x_val=check_x(x_diff);
												    	X_newval.setText(x_val[0]);;
												    	calibration("X_value", x_val[1], x_val[2], x_val[3], "0", "0");
													    }
												    
												   if(data.findInLine("Double: ")!=null){
												    	
												    	 System.out.println("" + data.nextLine());
												    	 System.out.println("X:" +x_change+ " Y:" +y_change+ " Z:" +z_change);
												    }
												    if(data.findInLine("OFF")!=null){
												    	
												    	data.close();
												    	
														Y_newval.setBackground(Color.white);
														X_newval.setBackground(Color.white);
												    	joystick.setEnabled(true);
												    	joystick.setForeground(Color.black);
												    	break;
												    }
												    
											}catch(NumberFormatException f) {
												System.out.println("Text box is Empty");
											}
												}
												
												System.out.println("Done.");
												serialPort.closePort();
												}catch(ArrayIndexOutOfBoundsException g) {
													JOptionPane.showMessageDialog(null, "Joystick is not connected.");	
													joystick.setEnabled(true);
													joystick.setForeground(Color.black);
												}	
											}
											
								};
								
								joystick.setEnabled(false);
								Thread t=new Thread(runner);
								t.start();
							
							}
							
						});            
									// Layout
									JPanel entries = new JPanel();
									entries.setName("Offset Calibration");
									entries.add(X_new);
									entries.add(Y_new);
									entries.add(X_newval);
									entries.add(Y_newval);
									entries.add(off_but);
									entries.add(close_cam);
									entries.add(joystick);
									entries.add(position);
									entries.add(avrgX);
									entries.add(avrgY);
									entries.add(exp_label);
									entries.setLayout(null);
									
									set_position(entries, exp_label, 100, 20);
									set_position(entries, X_new, 200, 150);
									set_position(entries, avrgX, 380, 150);
									set_position(entries, Y_new, 200, 200);
									set_position(entries, avrgY, 380, 200);
									set_position(entries, X_newval, 250, 150);
									set_position(entries, Y_newval, 250, 200);
									set_position(entries, off_but, 210, 400);
									set_position(entries, close_cam, 220, 350);
									set_position(entries, position, 520, 170);
									set_position(entries, joystick, 250, 300);
									entries.setVisible(true);
									offfid.setVisible(true);
									offfid.add(entries,BorderLayout.CENTER);
									}
								};
								
								Thread t=new Thread(runner);
								t.start();
						}
					});
					

					//"Done" button
					but_3.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							if (point1.getText().contains("Point") || point2.getText().contains("Point") || point3.getText().contains("Point")) {
								JOptionPane.showConfirmDialog(null, "No fiducials chosen, redo Step 1!","Fiducials input error",JOptionPane.CLOSED_OPTION);
							}
							else if (point1.getText().equals(point2.getText()) || point2.getText().equals(point3.getText()) || 
									point1.getText().equals(point3.getText())) {
								JOptionPane.showConfirmDialog(null, "Not enough fiducials chosen, redo Step 1!",
										"Fiducials input error",JOptionPane.CLOSED_OPTION);
							}
							else {                        		
								if (fid_cal<3) {
									fid_cal=fid_cal+1;
									
									 if (fid_cal==1) {
										but_5.setEnabled(true);
										x_tilt.set(0,Integer.valueOf(X_value.getText()));
										y_tilt.set(0,Integer.valueOf(Y_value.getText()));
										z_tilt.set(0,Integer.valueOf(Z_value.getText()));
										point1.setEnabled(false);
										point2.setEnabled(true);
										point2.setForeground(Color.red);
										ImageIcon image = new ImageIcon(dire+"/GUI_2.png");
										ima_lab.setIcon(image);
										x_off_fid1 = x_off;
										y_off_fid1 = y_off;
									}
									else if (fid_cal==2) {
										but_5.setEnabled(true);
										x_tilt.set(1,Integer.valueOf(X_value.getText()));
										y_tilt.set(1,Integer.valueOf(Y_value.getText()));
										z_tilt.set(1,Integer.valueOf(Z_value.getText()));
										point2.setEnabled(false);
										point3.setEnabled(true);
										point3.setForeground(Color.red);
										ImageIcon image = new ImageIcon(dire+"/GUI_3.png");
										ima_lab.setIcon(image);
										x_off_fid2 = x_off;
										y_off_fid2 = y_off;
										
									}
									else if (fid_cal==3) {
										but_5.setEnabled(true);
										x_tilt.set(2,Integer.valueOf(X_value.getText()));
										y_tilt.set(2,Integer.valueOf(Y_value.getText()));
										z_tilt.set(2,Integer.valueOf(Z_value.getText()));
										point3.setEnabled(false);
										but_3.setEnabled(false);
										but_4.setEnabled(true);
										ImageIcon image = new ImageIcon(dire+"/GUI_a.png");
										ima_lab.setIcon(image);
										x_off_fid3 = x_off;
										y_off_fid3 = y_off;
										
									}                                    
									  
									//................camera initialization..................................................................................
									
									x_cam = Integer.valueOf(X_value.getText());
									y_cam = Integer.valueOf(Y_value.getText());
									z_cam = Integer.valueOf(Z_value.getText());
									
									values = false;
									
									x_val = check_x(x_cam);
									y_val = check_y(y_cam);
									
									
									
									camera_fiducials(x_val[1],x_val[2],x_val[3],y_val[1],y_val[2], String.valueOf(z_cam),String.valueOf(x_off),String.valueOf(y_off));
									
									System.out.println(x_off);
									System.out.println(y_off);
									
									 /*Waiting Window*/ 
									  JFrame wait_frame = new JFrame("Running");
									  ImageIcon loading = new ImageIcon("waitme.gif");
									  wait_frame.add(new JLabel("Please Wait ...",loading,JLabel.CENTER));
									  wait_frame.setSize(300,300);
									  wait_frame.setVisible(true);
									  wait_frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
									  wait_frame.setAlwaysOnTop(true);
									  //wait_frame.setResizable(false);
									  wait_frame.setLocationRelativeTo(dia);
									  
									  Timer timer = new Timer(10000,new ActionListener(){
									  public void actionPerformed(ActionEvent e){
									  wait_frame.setVisible(true);
									  wait_frame.dispose();
									  }
									  });
									  timer.setRepeats(false);
									  timer.start();
									  
									 // Wait for the Template matching process
									
									try {
										Thread.sleep(10000);
									} catch (InterruptedException e2) {
										// TODO Auto-generated catch block
										e2.printStackTrace();
									}	  
									// File reader starts parsing for the offsets
 
							        String fileName = "fid_cam.txt";
							        
							        
							        try {
							        FileReader file = new FileReader(fileName);
							        
							        // Always wrap FileReader in BufferedReader.
							        BufferedReader bufferedReader =  new BufferedReader(file);
							        
							        int[] integers = new int [2];
							        int i=0;
							       
							            Scanner input = new Scanner(file);
							            while(input.hasNext())
							            {
							                integers[i] = input.nextInt();
							                i++;
							                
							            }
							            input.close();
							            
							        
							            
							            // Add the offsets to the previously calibrated positions
							         
							            x_tilt.set(fid_cal - 1,Integer.valueOf(X_value.getText()) + integers[0] );
										y_tilt.set(fid_cal - 1,Integer.valueOf(Y_value.getText()) + integers[1]);
										
										System.out.println(x_tilt);
										System.out.println("Failed");
										System.out.println(y_tilt);

							            // Always close files.
							            bufferedReader.close(); 
							            
							         
							        }
							        catch(FileNotFoundException ex) {
							        	
							        	JOptionPane.showConfirmDialog(null, "Unable to open file '" + fileName + "'","File not Found.",JOptionPane.CLOSED_OPTION);
							        	
							            System.out.println(
							                "Unable to open file '" + 
							                fileName + "'");
							           System.out.println(fid_cal);
							            fid_cal = 0;
							            
										point1.setEnabled(true);
										point1.setForeground(Color.red);
										point2.setEnabled(false);
										ImageIcon image = new ImageIcon(dire+"/GUI_1.png");
										ima_lab.setIcon(image);
											
							            
							        }
							        catch(IOException ex) {
							        	
							        	JOptionPane.showConfirmDialog(null, "Error reading file '" + fileName + "'","Wrong File Format.",JOptionPane.CLOSED_OPTION);

							            System.out.println(
							                "Error reading file '" 
							                + fileName + "'");                  
							            
							            fid_cal = 0;
							            
							            point1.setEnabled(true);
										point1.setForeground(Color.red);
										point2.setEnabled(false);
										ImageIcon image = new ImageIcon(dire+"/GUI_1.png");
										ima_lab.setIcon(image);
							            
							            // Or we could just do this: 
							            // ex.printStackTrace();
							        }
							       
							        lab_6.setText(fid_cal+" fiducial(s)");
							          
							        
							        }
									
								}
								calibration("Z_value", "0", "0", "0", "0", "0");
								
							}

						
					});

					//"Finish Calibration" button
					but_4.addActionListener(new ActionListener() {
						public void actionPerformed(ActionEvent e) {
							
							calibration("Move", "0", "0", "0", "0", "0");	
							
							x_average = (x_off_fid1 + x_off_fid2 + x_off_fid3) / 3;
							y_average = (y_off_fid1 + y_off_fid2 + y_off_fid3) /3;
							System.out.println(x_average);
							System.out.println(y_average);
							
							System.out.println("T0: "+x_tilt.get(0)+" "+y_tilt.get(0)+" "+z_tilt.get(0));
							System.out.println("T1: "+x_tilt.get(1)+" "+y_tilt.get(1)+" "+z_tilt.get(1));
							System.out.println("T2: "+x_tilt.get(2)+" "+y_tilt.get(2)+" "+z_tilt.get(2));
							
							String fid_s1=point1.getText();
							fid_1 = fid_s1.split("\\s+");
							String fid_s2=point2.getText();
							fid_2 = fid_s2.split("\\s+");
							String fid_s3=point3.getText();
							fid_3 = fid_s3.split("\\s+");
							System.out.println(x_tilt.get(0)+" "+y_tilt.get(0)+" "+z_tilt.get(0)
							+" "+x_tilt.get(1)+" "+y_tilt.get(1)+" "+z_tilt.get(1)
							+" "+x_tilt.get(2)+" "+y_tilt.get(2)+" "+z_tilt.get(2));

							String str =x_tilt.get(0)+" "+y_tilt.get(0)+" "+z_tilt.get(0)
							+" "+x_tilt.get(1)+" "+y_tilt.get(1)+" "+z_tilt.get(1)
							+" "+x_tilt.get(2)+" "+y_tilt.get(2)+" "+z_tilt.get(2)
							+" "+fid_1[1]+" "+fid_1[2]
							+" "+fid_2[1]+" "+fid_2[2]
							+" "+fid_3[1]+" "+fid_3[2];
							BufferedWriter writer;
							try {
								writer = new BufferedWriter(new FileWriter(dire+"/offset.txt"));
								writer.write(str);
								writer.close();
							} 
							catch (IOException e1) {
								e1.printStackTrace();
							}

							dia.dispose();

						}
					});

					JPanel butpan=new JPanel();
					butpan.add(tex);
					butpan.add(tex_1);
					butpan.add(but_1);
					butpan.add(tex_1c);
					butpan.add(tex_2);
					butpan.add(point1);
					butpan.add(point2);
					butpan.add(point3);
					butpan.add(ima_lab);
					butpan.add(but_2);
					butpan.add(lab_1);
					butpan.add(lab_2);
					butpan.add(lab_3);
					butpan.add(lab_4);
					butpan.add(lab_5);
					butpan.add(X_label);
					butpan.add(X_left_coarse);
					butpan.add(X_right_coarse);
					butpan.add(X_left_medium);
					butpan.add(X_right_medium);
					butpan.add(X_left_fine);
					butpan.add(X_right_fine);
					butpan.add(X_value);
					butpan.add(X_slider);
					butpan.add(Y_label);
					butpan.add(Y_left_coarse);
					butpan.add(Y_right_coarse);
					butpan.add(Y_left_medium);
					butpan.add(Y_right_medium);
					butpan.add(Y_left_fine);
					butpan.add(Y_right_fine);
					butpan.add(Y_value);
					butpan.add(Y_slider);
					butpan.add(Z_label);
					butpan.add(Z_up);
					butpan.add(Z_down);
					butpan.add(Z_value);
					butpan.add(Z_slider);
					butpan.add(but_3);
					butpan.add(lab_6);
					butpan.add(but_4);
					butpan.add(but_5);
					butpan.add(but_6);
					butpan.setLayout(null);
					set_position(butpan, tex, 320, 5);
					set_position(butpan, tex_1, 90, 30);
					set_position(butpan, but_1, 320, 65);
					set_position(butpan, tex_1c, 450, 65);
					set_position(butpan, tex_2, 75, 150);
					set_position(butpan, point1,155,205);
					set_position(butpan, point2,155,230);
					set_position(butpan, point3,155,255);
					set_position(butpan, ima_lab, 320,125);
					set_position(butpan, but_2, 125, 290);
					set_position(butpan, but_5, 125, 330);
					set_position(butpan, lab_1, 100, 375);
					set_position(butpan, lab_2, 200, 375);
					set_position(butpan, lab_3, 320, 375);
					set_position(butpan, lab_4, 400, 375);
					set_position(butpan, lab_5, 520, 375);
					set_position(butpan, X_label, 30, 405);
					set_position(butpan, X_left_coarse, 130, 405);
					set_position(butpan, X_right_coarse, 150, 405);
					set_position(butpan, X_left_medium, 230, 405);
					set_position(butpan, X_right_medium, 250, 405);
					set_position(butpan, X_left_fine, 315, 405);
					set_position(butpan, X_right_fine, 335, 405);
					set_position(butpan, X_value, 400, 405);
					set_position(butpan, X_slider, 520, 405);
					set_position(butpan, Y_label, 30, 455);
					set_position(butpan, Y_left_coarse, 130, 455);
					set_position(butpan, Y_right_coarse, 150, 455);
					set_position(butpan, Y_left_medium, 230, 455);
					set_position(butpan, Y_right_medium, 250, 455);
					set_position(butpan, Y_left_fine, 315, 455);
					set_position(butpan, Y_right_fine, 335, 455);
					set_position(butpan, Y_value, 400, 455);
					set_position(butpan, Y_slider, 520, 455);
					set_position(butpan, Z_label, 30, 505);
					set_position(butpan, Z_up, 315, 505);
					set_position(butpan, Z_down, 335, 505);
					set_position(butpan, Z_value, 400, 505);
					set_position(butpan, Z_slider, 520, 505);
					set_position(butpan, but_3, 360, 600);
					set_position(butpan, but_6, 360, 555);
					set_position(butpan, lab_6, 480, 605);
					set_position(butpan, but_4, 360, 640);

					dia.add(butpan,BorderLayout.CENTER);
				}               

			// SPIKE CHECK TOOL
				else if (cb.getSelectedIndex()==2) {
				
					dia=new JDialog();
					dia.setLocationRelativeTo(cp);
					dia.setSize(320,200);
					dia.setFont(new Font("Calibri", Font.PLAIN, 12));
					close(dia);

					int conf=JOptionPane.showConfirmDialog(null, "Finish Spike Check tool setup and Calibration?",
							"Setting up and Calibration confirmation",JOptionPane.YES_NO_OPTION);
					if (conf==JOptionPane.YES_OPTION) {
						dia.setVisible(true);
					}
					else {
						dia.dispose();
					}

					JButton sta = new JButton("Start");
					sta.setCursor(cusor);

					JButton pau= new JButton("Pause");
					pau.setCursor(cusor);

					JButton res = new JButton("Resume");
					res.setCursor(cusor);

					JButton sto = new JButton("Stop");
					sto.setCursor(cusor);

					pau.setEnabled(false);
					res.setEnabled(false);
					sto.setEnabled(false);

					sta.addActionListener(new ActionListener() {
						@Override
						public void actionPerformed(ActionEvent e) {
							Runnable runner = new Runnable() {
								public void run() {
									sta.setEnabled(false);
									pau.setEnabled(true);
									sto.setEnabled(true);
									//..........................
									x_average = -11717;
									y_average = 95;
									//..........................
									System.out.println(x_average);
									System.out.println(y_average);
									
									try {
										String val_x = String.valueOf(x_average);
										String val_y = String.valueOf(y_average);
										
										Runtime rt = Runtime.getRuntime();
							            Process proc = rt.exec("python move_spike.py" +" "+val_x+" "+val_y); 
										//Process proc = rt.exec("python test.py");
										//movespike((String.valueOf(x_average)),(String.valueOf(y_average)));
										
							            // any error message?
							            StreamGobbler errorGobbler = new 
							                StreamGobbler(proc.getErrorStream(), "ERROR");            
							            
							            // any output?
							            StreamGobbler outputGobbler = new 
							                StreamGobbler(proc.getInputStream(), "OUTPUT");
							                
							            // kick them off
							            errorGobbler.start();
							            outputGobbler.start();
							                                    
							            // any error???
							            int exitVal = proc.waitFor();
							            System.out.println("ExitValue: " + exitVal);        
							        } catch (Throwable t)
							          {
							            t.printStackTrace();
							          }
								}
							};
							Thread t=new Thread(runner);
							t.start();
						}
					});

					process_stat(pau, res, "Pause");
					process_stat(res, pau, "Resume");

					sto.addActionListener(new ActionListener() {
						@Override
						public void actionPerformed(ActionEvent e) {
							Runnable runner = new Runnable() {
								public void run() {
									sto.setEnabled(false);
									sta.setEnabled(true);
									pau.setEnabled(false);
									res.setEnabled(false);
									try {
										Runtime.getRuntime().exec("python "+dire+"/sta.py "+"Stop");
										Thread.sleep(1000);
										Runtime.getRuntime().exec("taskkill /im python.exe /f");
										//Runtime.getRuntime().exec("killall python");
									}
									catch (IOException e) {
										e.printStackTrace();
									} catch (InterruptedException e) {
										e.printStackTrace();
									}
								}
							};
							Thread t=new Thread(runner);
							t.start();
						}
					});

					JPanel butpan=new JPanel();
					butpan.add(sta);
					butpan.add(pau);
					butpan.add(res);
					butpan.add(sto);
					butpan.setLayout(null);
					set_position(butpan, sta, 135, 5);
					set_position(butpan, pau, 25, 50);
					set_position(butpan, res, 125, 50);
					set_position(butpan, sto, 225, 50);

					dia.add(butpan,BorderLayout.CENTER);
				}
			}
		});

		lab=new JLabel("                    ");
		lab.setBounds(100,100,150,30);

		cp.add(lab);
		cp.add(cb);
		cp.add(btn);

		menubar();

		setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
		addWindowListener(new WindowAdapter() {
			@Override
			public void windowClosing(WindowEvent e) {
				int conf=JOptionPane.showConfirmDialog(null, "Exit program?",
						"Exit confirmation",JOptionPane.YES_NO_OPTION);
				if (conf==JOptionPane.YES_OPTION) {
					dispose();
					if(dia != null) {
						dia.dispose();
					}
				}
			}
		});
		setTitle("Test");
		setSize(500,300);
		setVisible(true);   
		setDefaultLookAndFeelDecorated(true);
		setLocationRelativeTo(null);
	}

	public static void main(String[] args) {
		SwingUtilities.invokeLater(new Runnable() {
			@Override
			public void run() {
				new ComboBoxes();
					
			}
		});
	}
}