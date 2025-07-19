clear all;
close all;
clc;
numberOfBits=1024; %% Number of bits should be multiple integer of 8
data=randint(1,numberOfBits);
rData=reshape(data,numel(data)/8,8);
numberOfRows=numel(data)/8;
% semiData=[semiData ; ]
IV=[0,0,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,0,0,1,0,1,0,1,0,1,0,0,0,1,1];
IVD=IV; 
k= [1,0,1,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,1,0,0,1,1,1,0,0,1,0,1,0,0,1,0,0,0,0,1,0];

cipherText=[];
for i=1:1:numberOfRows
    i
  encryptedData=xor(IV,k);    
  encryptedMsg=xor(encryptedData(1:8),rData(i,:))
  cipherText=[cipherText;encryptedMsg]
  Shifting=[IV(9:64) encryptedData(1:8)];
  IV=Shifting;
end
 plainText=[];

 for j=1:1:numberOfRows
     j
     decryptedData=xor(IVD,k);
     decryptedMsg=xor(decryptedData(1:8),cipherText(j,:));
     plainText=[plainText;decryptedMsg];
     Shifting=[IVD(9:64) decryptedData(1:8)];
     IVD=Shifting;
 end
 
 plainTextFinal=reshape(plainText,1,numel(plainText));
 [noOfError BER]=biterr(data,plainTextFinal)
