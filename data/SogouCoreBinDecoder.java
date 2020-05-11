import java.io.*;
import java.nio.*;
import java.nio.channels.*;
import java.util.*;
import java.lang.*;
import java.text.*;

public class SogouCoreBinDecoder {
    public static void main(final String[] args) throws IOException {
	    final String version = "9.2";
	    final String binFile = "./SogouWordlibs/sgim_core-v"+version+".bin";
//	    final String txtFile = "./SogouCoreWordlib-v"+version+".txt";
	    final String txtFile = "wordlib.txt";
	}
    
    public static void ConvertBinToTxt(String binFile,String txtFile) {
	    final List<String> wordlist = new ArrayList<String>();
	    final int[] searchKey = { 0x02, 0x00, 0x4A, 0x55 }; 
	    final ByteBuffer bb;
	    try (RandomAccessFile file = new RandomAccessFile(binFile, "r"); final FileChannel fChannel = file.getChannel();) {
	        bb = ByteBuffer.allocate((int) fChannel.size());
	        fChannel.read(bb);
	    }
 
	    bb.order(ByteOrder.LITTLE_ENDIAN);
	    bb.rewind();

	    int words = bb.getInt(0xC);
	    System.out.println("读入文件: " + binFile + "，单词：" + words);
	    int idx = 0;
	    int i;
	    int startPos = -1;
	    while (bb.hasRemaining()) {
	        i = 0xff & bb.get();
	        if (i == searchKey[idx]) {
	            idx++;
		        if (idx == searchKey.length) {
		            startPos = bb.position() - searchKey.length;
		            break;
		        }
	        }
	        else idx = 0;
	    }

	    if (startPos != -1) {
	        short s;
	        int counter = 0;
	        String perc;
	        final ByteBuffer buffer = ByteBuffer.allocate(Short.MAX_VALUE);
	        System.out.println("单词起始位置：0x" + Integer.toHexString(startPos));
	        bb.position(startPos); 
	        NumberFormat numberFormat = NumberFormat.getInstance();  
	        numberFormat.setMaximumFractionDigits(2);
	        while (bb.hasRemaining() && counter<words) {
	            s = bb.getShort();
	            bb.get(buffer.array(), 0, s);
	            counter++;
	            String word = new String(buffer.array(), 0, s, "UTF-16LE");
	            perc = numberFormat.format((float)counter*100/(float)words);
	            if(word.length() > 1){
	                wordlist.add(word);
	                System.out.print("\r [Words]: "+counter+"  [Percentage]: "+perc+"%");
	            }
	        }
	        System.out.println("\n");
	        
	        final int endPos = bb.position();
	        final int diff = endPos - startPos;
	        System.out.println("读出单词'" + binFile + "'：" + counter);
	        System.out.println("单词结尾位置：0x" + Integer.toHexString(endPos));
	        System.out.println("单词词典长度：0x" + Integer.toHexString(diff));
	    } else {
	        System.err.println("文件版本已更新！");
	    }
	      
	    try{
	        BufferedWriter writer = new BufferedWriter(new FileWriter(new File(txtFile),true));
	        writer.write(String.join("\n", wordlist)+"\n");
	        System.out.println("Words Saved to "+txtFile);
	        writer.close();
	    }catch(Exception e){
	        e.printStackTrace();
	    }
	}

}