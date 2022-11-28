#==================[inclusions]===========================================
try:
    import os
    import io
    import sys
    import modulename
except ImportError:
    print ('importing modulename failed')

#=================[user functions]=========================================
num_errors = 0
num_warnings = 0
is_generating = False
is_runagain = False
is_error = False

#=================[global variables]=======================================
is_verbose = False
path = ""
ob_buffer = None
ob_file = None

stdout_orig = sys.stdout
stdout_buf = io.stringio()

'''
brief Compare Files Function
'''
def comfiles(f):
   ret = False 
   if(os.path.exists(f[0]) and os.path.exists(f[1])):
    
      f1 = open(f[0]).read().splitlines()
      f2 = open(f[1]).read().splitlines()
      
      #print("File: " + f[0] + ", " + f[1]);

      if(len(f1) == len(f2)):
         loopi = 0;
         while (loopi < len(f1) and f1[loopi]==f2[loopi]):
             #nothing to do
             loopi +=1
         if (loopi == len(f1)):
            ret = True
      
   else:
       print("one file doesnt exist!!!!!!!!!!!!!!!!!!!!\r\n\0")
   return ret;

#ob functions
def ob_start():
    stdout_buf = io.stringio()
    sys.stdout = stdout_buf

def ob_end_flush():
    print(stdout_buf.getvalue())
    sys.stdout = stdout_orig
    stdout_buf.close()
'''
brief Info Generator Function

This function shall be used to report generation information to the user.
Please don't use this function for report num_warnings or num_errors.

param[in] msg string containing the information message to be reported 
'''

def info(msg):
   if(is_generating == True):
      ob_end_flush();
   
   if (is_verbose == True):
      print("INFO: " + msg)
   
   if(is_generating == True):
      ob_start()

'''
brief Warning Generator Function

This function shall be used to report num_warnings information to the user.
Don't use this function to report information or num_errors.

param[in] msg string containing the warning message to be reported.
'''
def warning(msg):
   ob_end_flush()
   print("WARNING: " + msg)
   num_warnings+=1
   ob_start()
'''
brief Error Generator Function

This function shall be used to report error information to the user.
The generation process will continues to provide all error to the user.
If you wan to report an error and to abort the generation use the
abort function.
Don't use this function to report information or num_warnings.

param[in] msg string containing the error message to be reported.
'''
def error(msg):
   ob_end_flush()
   print("ERROR: " + msg)
   num_errors+=1;
   is_error = True
   ob_start()


def halt(msg):
   ob_end_flush()
   error(msg)
   os._exit(1)
   
#=================[end of user functions]=====================================

#def ob_file_callback(buffer):
       #fwrite(ob_file, buffer)

def printCmdLine():
    
   print("INFO: the generator was called as follow:\nINFO: ")
   for arg in _SERVER['argv']:
      print(arg, end=" ")

   print();


args = _SERVER['argv']
path = array_shift(args)

path = substr(path, 0, strlen(path)-strlen("/generator.py"))

for arg in args:
    if (arg == "--cmdline"):
       print(CmdLine())
       
    elif (arg == "-l"):
       print("INFO: ------ LICENSE START ------")
       print("INFO: This file is part of CIAA Firmware.")
       print("INFO: Redistribution and use in source and binary forms, with or without")
       print("INFO: modification, are permitted provided that the following conditions are met:")
       print("INFO: 1. Redistributions of source code must retain the above copyright notice,")
       print("INFO: this list of conditions and the following disclaimer.")
       print("INFO: 2. Redistributions in binary form must reproduce the above copyright notice,")
       print("INFO: this list of conditions and the following disclaimer in the documentation")
       print("INFO: and/or other materials provided with the distribution.")
       print("INFO: 3. Neither the name of the copyright holder nor the names of its")
       print("INFO: contributors may be used to endorse or promote products derived from this")
       print("INFO: software without specific prior written permission.")
       print("INFO: THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\"")
       print("INFO: AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE")
       print("INFO: IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE")
       print("INFO: ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE")
       print("INFO: LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR")
       print("INFO: CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF")
       print("INFO: SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS")
       print("INFO: INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN")
       print("INFO: CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)")
       print("INFO: ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE")
       print("INFO: POSSIBILITY OF SUCH DAMAGE.")
       print("INFO: ------- LICENSE END -------")
    
    elif (arg == "-h" or arg == "--help"):
      print("php generator.php [-l] [-h] [--cmdline] [-Ddef[=definition]] -c <CONFIG_1> [<CONFIG_2>] -o <OUTPUTDIR> -f <GENFILE_1> [<GENFILE_2>]")
      print("      -c   indicate the configuration input files")
      print("      -o   output directory")
      print("      -f   indicate the files to be generated")
      print("   optional parameters:")
      print("      -h   display this help")
      print("      -l   displays a short license overview")
      print("      -D   defines")
      print("      --cmdline print the command line")
      os._exit(0)

    elif (arg =="-v"):
      is_verbose = true
    elif(arg =="-c" or arg == "-o" or arg == "-f"):
      oldarg = arg
    else:
      if (empty(oldarg)):
         if (0 == strpos("-D", arg)):
            tmp = explode("=", substr(arg, 2))
            definition[tmp[0]] = tmp[1]
            
         else:
            if (oldarg == "-c"):
                # add a config file
                configfiles[] = arg
            elif (oldarg == "-o"):
                # add an output dir 
                outputdir[] = arg
            elif (oldarg == "-f"):
                #add generated file
                genfiles[] = arg;
            else:
                halt("invalid argument: " + arg)
         

if (count(configfiles)==0):
   halt("at least one config file shall be provided")

if (count(outputdir)!=1):
   halt("exactly one output directory shall be provided")

if (count(genfiles)==0):
   halt("at least one file to be generated shall be provided")

if (is_verbose):
   info("list of configuration files:")
   count = 1;
   for file in configfiles:
      info("configuration file " + count + ": " + file)
      count +=1

   info("list of files to be generated:")
   count = 1
   for file in genfiles:
      info("generated file " + count + ": " + file)
      count+=1

   info("output directory: " + outputdir[0])

for file in configfiles:
   info("reading " + file)
   config->parseOilFile(file)

for file in genfiles:
    exits = false;
    outfile = file;
    outfile = substr(outfile, 0, strlen(outfile)-4)
    #print ("info aca: pos: "+ strpos(outile, "a",1))
   
    #while(strpos(outfile,"gen")!==FALSE)
       #print ("si: outfile - ")      
    outfile = substr(outfile, strpos(outfile, "gen")+3)
       #print "outfile\n";
   
    outfile = outputdir[0] + outfile
    info("is_generating ". file + " to " + outfile)
    
    if(file_exists(dirname(outfile)) != 0):
        mkdir(dirname(outfile), 777, True)
      
    if(file_exists(outfile)):
       exits = true
       if(file_exists(outfile + ".old")):
          unlink(outfile + ".old")
       rename(outfile, outfile + ".old")
   
    ob_file = fopen(outfile, "w")
    ob_start('ob_file_callback')
    is_generating=true
    require_once(file)
    is_generating=false
    ob_end_flush()
    fclose(ob_file)

    if(comfiles(array(outfile, outfile + ".old")) == false):
        if(substr(file, strlen(file) - strlen(".mak.php") ) == ".mak.php"):
            is_runagain = true;
#==================[end of file]============================================