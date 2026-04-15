# Sample unified diff: Subu30.pas (root vs doseryutong/book_07 buk-and-buk)

```diff
--- /Users/speeno/Delphi_porting/WeLove_FTP/도서유통-New/Subu30.pas	2026-04-13 14:05:08
+++ /Users/speeno/Delphi_porting/WeLove_FTP/도서유통-New/도서유통/book_07(북앤북)/Subu30.pas	2026-04-13 14:05:08
@@ -5,13 +5,14 @@
 uses
   Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
   OleCtrls, SHDocVw, dxCore, dxButtons, ExtCtrls, ActiveX, ComObj, ShellApi,
-  StdCtrls, Mylabel, acPNG;
+  StdCtrls, Mylabel;
 
 type
   TSobo30 = class(TForm)
     Button100: TdxButton;
     Image1: TImage;
     myLabel3d1: TmyLabel3d;
+    myLabel3d2: TmyLabel3d;
     procedure FormActivate(Sender: TObject);
     procedure FormShow(Sender: TObject);
     procedure FormClose(Sender: TObject; var Action: TCloseAction);
@@ -244,8 +245,8 @@
 
 procedure TSobo30.myLabel3d1Click(Sender: TObject);
 begin
-  ShellExecute(Handle,'Open','http://www.yeskb.com',nil,nil,SW_Show);
-//NavigateIE('http://www.yeskb.com');
+  ShellExecute(Handle,'Open','http://www.suresa.co.kr/',nil,nil,SW_Show);
+//NavigateIE('http://www.suresa.co.kr/');
 end;
 
 end.

```
