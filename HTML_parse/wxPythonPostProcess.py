import wx
import os
import re
import ParseHTMLTable

ID_TEXTCTRL = 10000
ID_TEXT = 10001
ID_SCROLLED = 10002
ID_BUTTON = 10003
frameSize = (500,500)
myLightGrey = [211,211,211]
myDarkGrey = [122,138,144]

# For LEED
#TEMPLATEPATH = os.path.normpath(r"D:\Freelancing\01_AutomatedReporting\postProcessTemplateLEED r01.xlsx")
# For Estidama
TEMPLATEPATH = os.path.normpath(r"D:\Freelancing\01_AutomatedReporting\postProcessTemplateEstidama r02.xlsx")

#XLTARGETPATH= os.path.normpath(r"D:\Freelancing\Simulation\\00VariantsPostProcess.xlsx")
thisProjDir = r"D:\Freelancing\Simulation\\"
#thisProjDir = r"D:\Freelancing\Simulation\FirstHalf\\"
PROJECTDIR = os.path.normpath(thisProjDir)
XLTARGETPATH =  os.path.normpath(thisProjDir + r"\\00VariantsPostProcess.xlsx")


import logging.config
logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')

class MyFrame(wx.Frame):
    """ Derive a new class of Frame. """
    def __init__(self, parent, title="EXERGY Studio", call_fit = True, set_sizer = True):
        
        self.mySearchPath = PROJECTDIR
        self.myHTMLfiles = list()
        self.templatePath = TEMPLATEPATH
        self.xlTargetPath = XLTARGETPATH
        
        #=======================================================================
        # Initialize wx.Frame
        #=======================================================================
        wx.Frame.__init__(self, parent, title=title, size=frameSize) 
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        
        
        #=======================================================================
        # Background color
        #=======================================================================
        self.SetBackgroundColour(myDarkGrey)
        
        #=======================================================================
        # Status bar
        #=======================================================================
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        
        #=======================================================================
        # Setting up the menu.
        #=======================================================================
        filemenu= wx.Menu() 
        
        # Create the about and exit
        menuOpenFile = filemenu.Append(wx.ID_OPEN,"&Open file"," Open a file") 
        menuOpenDir = filemenu.Append(wx.ID_OPEN,"Open dir"," Open a directory") 
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program") 
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program") 
        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.

        # Creating the menubar.
        menuBar = wx.MenuBar() 
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        
        # Bind the menu items
        # Bind self.MyFunction to an oject, through EVT_MENU
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)        
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit) 
        #self.Bind(wx.EVT_MENU, self.OnOpenFile, menuOpenFile) 
        self.Bind(wx.EVT_MENU, self.OnOpenDir, menuOpenDir) 
                
        self.Show(True)
        

        #=======================================================================
        # LAYOUT
        #=======================================================================
        item0 = wx.BoxSizer( wx.VERTICAL )
        
        # Space
        item0.Add( [ 20, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        # Text
        item1 = wx.StaticText( self, ID_TEXT, "The output directory for HTML summary files", wx.DefaultPosition, wx.DefaultSize, 0 )
        item0.Add( item1, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
        
        # Text box
        self.searchPathBoxCtrl = wx.TextCtrl(self, ID_TEXTCTRL, "", wx.DefaultPosition, [300,-1], wx.TE_READONLY )
        self.searchPathBoxCtrl.SetBackgroundColour( myLightGrey )
        item0.Add( self.searchPathBoxCtrl, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
        
        # Text
        item1 = wx.StaticText( self, 10010, "Excel template", wx.DefaultPosition, wx.DefaultSize, 0 )
        item0.Add( item1, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
        
        # Text box
        self.templatePathBoxCtrl = wx.TextCtrl(self, 10011, "", wx.DefaultPosition, [300,-1], wx.TE_READONLY )
        self.templatePathBoxCtrl.SetBackgroundColour( myLightGrey )
        item0.Add( self.templatePathBoxCtrl, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
                
         # Text
        item1 = wx.StaticText( self, 10010, "Excel Target", wx.DefaultPosition, wx.DefaultSize, 0 )
        item0.Add( item1, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
        
        # Text box
        self.xlTargetPathBoxCtrl = wx.TextCtrl(self, 10011, "", wx.DefaultPosition, [300,-1], wx.TE_READONLY )
        self.xlTargetPathBoxCtrl.SetBackgroundColour( myLightGrey )
        item0.Add( self.xlTargetPathBoxCtrl, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
                
               
        
        # Space
        item0.Add( [10, 10 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )
       
        # Text
        item1 = wx.StaticText( self, ID_TEXT, "HTML Table files in directory", wx.DefaultPosition, wx.DefaultSize, 0 )
        item0.Add( item1, 0, wx.ALIGN_LEFT|wx.ALL, 5 )

#        # Scroll box
#        self.myScrollCtrl = wx.TextCtrl( self, ID_TEXTCTRL, "", wx.DefaultPosition, [300,200], wx.TE_MULTILINE )
#        self.myScrollCtrl.SetBackgroundColour( myLightGrey )
#        item0.Add( self.myScrollCtrl, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
#       
        self.myListBox = wx.ListBox(self, 26, wx.DefaultPosition, (170, 130), self.myHTMLfiles, wx.LB_EXTENDED)        
        self.myListBox.SetBackgroundColour( myLightGrey )
        item0.Add( self.myListBox, 0, wx.ALIGN_LEFT|wx.ALL, 5 )        
        
        self.myParseButton = wx.Button( self, ID_BUTTON, "Parse selection", wx.DefaultPosition, wx.DefaultSize, 0 )
        item0.Add( self.myParseButton, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.myParseButtonClick, self.myParseButton)


        self.myOpenExcelButton = wx.Button( self, 10050, "Open the excel file", wx.DefaultPosition, wx.DefaultSize, 0 )
        item0.Add( self.myOpenExcelButton, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.myOpenExcelButtonClick, self.myOpenExcelButton)
       
#        self.myScrollCtrl = wx.ScrolledWindow( self, ID_SCROLLED, wx.DefaultPosition, [200,160], wx.VSCROLL )
#        self.myScrollCtrl.SetBackgroundColour( myLightGrey )
#        self.myScrollCtrl.SetScrollbars( 10, 10, 20, 100, 0, 0 )
#        item0.Add( self.myScrollCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        if set_sizer == True:
            #print 
            self.SetSizer( item0 )
            if call_fit == True:
                item0.SetSizeHints( self )
        #===========================================================================
        # FIRST TIME  
        #===========================================================================
        print self.mySearchPath
        self.searchPathBoxCtrl.SetValue(self.mySearchPath)
        self.myHTMLfiles = ParseHTMLTable.locateHTMLfiles(self.mySearchPath)
        self.SetStatusText("Loaded {0} HTML files from directory".format(len(self.myHTMLfiles)))

        self.myListBox.Set(self.myHTMLfiles)
        print len(self.myHTMLfiles)
        
        for i in range(0,self.myListBox.GetCount()):
            self.myListBox.SetSelection(i,True)
        
        self.templatePathBoxCtrl.SetValue(self.mySearchPath)
        
        self.templatePathBoxCtrl.SetValue(self.templatePath)
        
        self.xlTargetPathBoxCtrl.SetValue(self.xlTargetPath)

        
    #===========================================================================
    # The events    
    #===========================================================================
             
    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "A small text editor", "About Sample Editor", wx.OK) 
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnOpenDir(self,e):
        """ Open a dir"""
        #self.dirname = '..'
        dlg = wx.DirDialog(self, "Choose directory")
        if dlg.ShowModal() == wx.ID_OK:
            self.mySearchPath = dlg.GetPath()
            print self.mySearchPath
            #f = open(os.path.join(self.dirname, self.filename), 'r')
            #self.control.SetValue(f.read())
            #f.close()
            self.searchPathBoxCtrl.SetValue(self.mySearchPath)
            self.myHTMLfiles = ParseHTMLTable.locateHTMLfiles()
            #print self.myHTMLfiles
            #HTMLfileText = "\n".join(self.myHTMLfiles)
            #print HTMLfileText
            #self.myScrollCtrl.SetValue("Loaded {0} HTML files".format(len(self.myHTMLfiles)))
            self.SetStatusText("Loaded {0} HTML files from directory".format(len(self.myHTMLfiles)))
            
            self.myListBox.Set(self.myHTMLfiles)
            print len(self.myHTMLfiles)
            
            for i in range(0,self.myListBox.GetCount()):
                self.myListBox.SetSelection(i,True)
            
#            for(size_t i = 0; i < listBox->GetCount(); i++)
#                listBox->SetSelection(i, true);
#            
            
            #self.myListBox.SetSelection(len(self.myHTMLfiles))
        dlg.Destroy()

        

#    def OnOpenFile(self,e):
#        """ Open a file"""
#        self.dirname = '..'
#        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
#        if dlg.ShowModal() == wx.ID_OK:
#            self.filename = dlg.GetFilename()
#            self.dirname = dlg.GetDirectory()
#            print self.dirname, self.filename
#            f = open(os.path.join(self.dirname, self.filename), 'r')
#            #self.control.SetValue(f.read())
#            f.close()
#        dlg.Destroy()

#    def loadHTMLfiles(self):
#        # Locate the HTML table files
#        tableFileNames = list()
#        for name in os.listdir(self.mySearchPath):
#            if re.search("Table.html$",name):
#                #print name
#                #logging.info("Found {0}".format(name))
#                tableFileNames.append(name)        
#
#        self.myHTMLfiles = tableFileNames

    def myOpenExcelButtonClick(self,e):
        ParseHTMLTable.simpleOpenExcel(self.xlTargetPath)
        
        
    def myParseButtonClick(self,e):
        # Locate the HTML table files
        #self.myScrollCtrl.SetValue("Processing {0} HTML files".format(len(self.myHTMLfiles)))
        
        selectedItems = self.myListBox.GetSelections()

        mySubsetHTMLFiles = [self.myHTMLfiles[i] for i in selectedItems]

        self.SetStatusText("Processing {0} HTML files".format(len(mySubsetHTMLFiles)))
        
        print mySubsetHTMLFiles
        
        self.myVariants = ParseHTMLTable.parseFilesIntoVariants(self.mySearchPath, mySubsetHTMLFiles)
        
        self.SetStatusText("Permuting {0} HTML files".format(mySubsetHTMLFiles))

        self.myVariants = ParseHTMLTable.permuteEstidama(self.myVariants)

        ParseHTMLTable.writeExcel(self.templatePath, self.xlTargetPath, self.myVariants )
        
        self.SetStatusText("Wrote {} ".format(self.xlTargetPath))

#logging.config.fileConfig('..\\LoggingConfig\\logging.conf')

logging.info("Start")

app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window. @UndefinedVariable
frame = MyFrame(None) # None is the parent # A Frame is a top-level window.
frame.Show(True)     # Show the frame.
app.MainLoop()