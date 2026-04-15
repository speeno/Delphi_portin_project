unit Seok09;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  IniFiles, ShellAPI, IdBaseComponent, IdComponent, IdTCPConnection,
  IdTCPClient, IdFTP, ExtCtrls, Buttons, CheckLst, StdCtrls, ComCtrls,
  FileCtrl, IdAntiFreezeBase, IdAntiFreeze;

type
  TSeok90 = class(TForm)
    Shape1: TShape;
    Panel1: TPanel;
    Label3: TLabel;
    lbWait: TLabel;
    LabelCount2: TLabel;
    ProgressBar1: TProgressBar;
    CheckListBox1: TCheckListBox;
    Panel2: TPanel;
    btnConnect: TSpeedButton;
    btnDisConnect: TSpeedButton;
    btnClose: TSpeedButton;
    btndown: TSpeedButton;
    Panel3: TPanel;
    Timer1: TTimer;
    IdFTP1: TIdFTP;
    LabelCount1: TLabel;
    Label1: TLabel;
    Label2: TLabel;
    ListBox1: TFileListBox;
    IdAntiFreeze1: TIdAntiFreeze;
    procedure ParseFtpDirList(dirList: string);
    procedure DeleteSpace(var str: string);
    procedure btnConnectClick(Sender: TObject);
    procedure NMFTP1ListItem(Listing: String);
    procedure btnCloseClick(Sender: TObject);
    procedure btnDisConnectClick(Sender: TObject);
    procedure btndownClick(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure IdFTP1Work(Sender: TObject; AWorkMode: TWorkMode; const AWorkCount: Integer);
    procedure IdFTP1WorkBegin(Sender: TObject; AWorkMode: TWorkMode; const AWorkCountMax: Integer);
    procedure IdFTP1WorkEnd(Sender: TObject; AWorkMode: TWorkMode);
  private
    FClientInstance, FPrevClientProc : TFarProc;
    STime: TDateTime;
    BytesToTransfer: LongWord;
    { Private declarations }
  public
    gHost, gPort, gUserID, gPassword : string;
    gExeFile, gPath, fPath, hPath: string;
    gFile : String; //압축파일이름
    function FormatNumber(l:longint):string;
    function GetExePath:string;
    function ConnectToHost: Boolean;
    function ConnectToChck: Boolean;
    { Public declarations }
  end;

TFTPDirList = packed record
  FileAuth : string;
  FileName : string;
  FileSize : string;
  FileDate : string;
  FileTime : integer;
  FileDirs : Boolean;
end;

var
  Seok90: TSeok90;
  FTPList : TFTPDirList;
  FCount1 : integer;
  FCount2 : integer;

implementation

uses Chul, Subu38;

Const
  AverageSpeed: Double = 0;

{$R *.DFM}

function TSeok90.GetExePath:string;
var LastBackSlashPos, i : integer;
begin
  LastBackSlashPos := 0;
  Result := Application.ExeName;
  for i := 1 to Length(Result) do begin
    if Result[i] = '\' then
       LastBackSlashPos := i;
  end;
  Result := Copy(Result, 1, LastBackSlashPos - 1);
end;

procedure TSeok90.btnConnectClick(Sender: TObject);
const
   IniName = 'Downcfg.ini';
var
   DBCFG: TIniFile;
   ExePath : String;
begin
  ExePath   := GetExePath;
  gPath     := ExePath + '\Remote\';
  DBCFG     := TIniFile.Create(ExePath + '\Config.ini');
  gHost     := DBCFG.ReadString('DownLoad','FTPHOST','');
  fPath     := DBCFG.ReadString('DownLoad','FTPPATH','');
  gPort     := DBCFG.ReadString('DownLoad','FORT','');
  gUserID   := DBCFG.ReadString('DownLoad','USERID','');
  gPassword := DBCFG.ReadString('DownLoad','PASSWORD','');
  gExeFile  := DBCFG.ReadString('DownLoad','ExeFile','');  // 프로그램 샐행 파일
  gFile     := DBCFG.ReadString('DownLoad','gFile','');    //압축파일

//  if IdFTP1.Connected = False then
//     ConnectToHost;
end;

function TSeok90.ConnectToHost: Boolean;
var
   i : Integer;
begin
  CheckListBox1.Clear;
  Result:= True;
  IdFTP1.Host := gHost;
  IdFTP1.Port := StrToInt(gPort);
  IdFTP1.Username := gUserID;
  IdFTP1.Password := gPassword;
  try
    IdFTP1.Disconnect;
    IdFTP1.Connect;
    IdFTP1.ChangeDir(hPath);
    Panel3.Caption := '호스트에 접속되었습니다!.';
    except On E:Exception do begin
       ShowMessage('FTP 서버 ' + gHost + ' 에 연결할 수 없습니다...' + #13#10 + E.Message);
       Panel3.Caption := gHost + ' 연결실패!!! 관리자에게 문의하세요...';
       Exit;
    end;
  end;
  IdFTP1.List(ListBox1.Items,'*.txt');
  for i := ListBox1.Items.Count - 1 downTo 0 do begin
    CheckListBox1.Items.Add(Trim(Copy(ListBox1.Items[i], 40, 20)));
  end;
end;

function TSeok90.ConnectToChck: Boolean;
var
   i : Integer;
begin
  IdFTP1.Noop;
  CheckListBox1.Clear;
  Result:= True;
  IdFTP1.List(ListBox1.Items,'*.txt');
  for i := ListBox1.Items.Count - 1 downTo 0 do begin
    CheckListBox1.Items.Add(Trim(Copy(ListBox1.Items[i], 40, 20)));
  end;
end;

procedure TSeok90.NMFTP1ListItem(Listing: String);
begin
  if not (Pos('<DIR>',  Listing) > 0) then begin
    ListBox1.Items.Add(Listing);
    CheckListBox1.Items.Add(Trim(Copy(Listing, 40, 20)));
  end;
end;

procedure TSeok90.btnCloseClick(Sender: TObject);
begin
  Close;
end;

procedure TSeok90.btnDisConnectClick(Sender: TObject);
begin
  if IdFTP1.Connected = True then begin
     IdFTP1.Disconnect;
     Panel3.Caption := '호스트와의 연결이 끊어졌습니다!.';
     ListBox1.Clear;
  end;
end;

function TSeok90.FormatNumber(l:longint):string;
begin
  FormatNumber:=FormatFloat('#,##0',StrToFloat(IntToStr(l)));
end;

procedure TSeok90.DeleteSpace(var str: string);
var i, idx: integer;
begin
  for i := 1 to Length(str) do begin
    if str[i] <> ' ' then begin
      idx := i - 1;
      break;
    end;
  end;
  Delete(str, 1, idx);
end;

procedure TSeok90.ParseFtpDirList(dirList: string);
var
 i: integer;
 idx: integer;
begin
  FillChar(FTPList, sizeof(TFTPDirList), 0);
  i:=StrToInt(dirList);
  { FILE OR DIR NAME }
  FTPList.FileName := idFTP1.DirectoryListing.Items[i].FileName;
  { 날짜 }
  FTPList.FileDate := FormatDateTime('YYYY-MM-DD hh:mm:ssAM/PM', idFTP1.DirectoryListing.Items[i].ModifiedDate);
  { 파일 크기 }
  FTPList.FileSize := IntToStr(idFTP1.DirectoryListing.Items[i].Size);
end;

procedure TSeok90.btndownClick(Sender: TObject);
var
   FHandle, i , j: Integer;
   Temp, HH : String;
   cDate, sDate : TDateTime;
   FileName : String;
   ServerDT : string;
   Save_Cursor:TCursor;
   tMsg, eMsg : String;

   SearchRec: TSearchRec;
   FileTime : Integer;
   FileSize, FileDate : String;

   SendDate : String;

   MemoryStream: TMemoryStream;
begin
 //if(Application.MessageBox('프로그램을 다운 받으시겠습니까?','확인', MB_OKCANCEL) <> IDOK)then Exit;
   if IdFTP1.Connected = True then begin
      if(gHost = '')then begin
         ShowMessage('INI파일에 서버IP를 등록하세요...');
         Exit;
      end;
      tMsg := '';
      eMsg := '';

      SendDate:=Copy(Sobo38.Edit101.Text,1,4)+Copy(Sobo38.Edit101.Text,6,2)+Copy(Sobo38.Edit101.Text,9,2);

      idFTP1.List(ListBox1.Items,'*.txt');//  <=== 스트링 리스트에 LS 결과를 받아옴..
      for i := ListBox1.Items.Count - 1 downTo 0 do begin
         ParseFtpDirList(IntToStr(i));
         FileName := FTPList.FileName;
         FileSize := '';
         FileDate := '';
         Label3.Caption:= '파일명 : ' + FileName;
      //if Pos(nCode,ExtractFileName(FTPList.FileName))<>0 then begin
         if FindFirst(FileName,faAnyFile,SearchRec) = 0 then begin
            FileSize	:= IntToStr(SearchRec.Size);
            FileTime	:= SearchRec.Time;
         // FileDate    := DateToStr(FileDateToDateTime(SearchRec.Time));
         // FileDate    := DateTimeToStr(FileDateToDateTime(SearchRec.Time));
            FileDate    := FormatDateTime('YYYY-MM-DD hh:mm:ssAM/PM',FileDateToDateTime(SearchRec.Time));
            FindClose(SearchRec);
         end;
         //Server File DateTime저장
         Temp := FTPList.FileDate;
         if Copy(Temp, 20, 2) = 'AM' then
            HH := Copy(Temp, 12, 2)
         else begin
            if StrToInt(Copy(Temp, 12, 2)) = 12 then
            HH := Copy(Temp, 12, 2) else
            HH := Format('%.02d',[StrToInt(Copy(Temp, 12, 2))+12]);
         end;
         ServerDT:=Copy(Temp,1,11)+HH+Copy(Temp,14,6);
         sDate := StrToDateTime(ServerDT);

            { Sobo38.Memo2.Clear;
              Sobo38.Memo2.Lines.LoadFromFile(FTPList.FileName);

              Sobo38.T3_Sub82.Insert;
              Sobo38.T3_Sub82.FieldByName('Memo2').Assign( Sobo38.Memo2.Lines );
              Sobo38.T3_Sub82.Post; }

         if Pos(SendDate,FTPList.FileName) > 0 then
         if(FTPList.FileSize<>FileSize)or(FTPList.FileDate<>FileDate)then begin
         // ShowMessage(FTPList.FileSize+' '+FileSize+' '+FTPList.FileDate+' '+FileDate);
            try
              eMsg := '1';
              Save_Cursor := Screen.Cursor;
              ProgressBar1.Position := 0;
            //IdFTP1.TransferType := ftBinary;
              Screen.Cursor:= crHourGlass;
              Panel3.Caption := '파일을 받고 있습니다!.';
            //BytesToTransfer := IdFTP1.Size(CheckListBox1.Items.Strings[i]);
            //IdFTP1.Get(CheckListBox1.Items.Strings[i],CheckListBox1.Items.Strings[i],True);
            //IdFTP1.Get(FileName, FileName,True);
            //IdFTP1.Put(gPath+FileName, FileName);

              MemoryStream := TMemoryStream.Create;
              IdFTP1.Get(FileName, MemoryStream, True);

              Sobo38.T3_Sub82.Edit;
              Sobo38.T3_Sub82Memo1.LoadFromStream(MemoryStream);
              Sobo38.T3_Sub82Memo2.LoadFromStream(MemoryStream);
              Sobo38.T3_Sub82.Post;

              MemoryStream.Free;


            { Sobo38.T3_Sub82.Edit;
              Sobo38.T3_Sub82Memo1.LoadFromFile(FileName);
              Sobo38.T3_Sub82Memo2.LoadFromFile(FileName);
              Sobo38.T3_Sub82.Post; }

            //DownLoad완료후 Client화일의 DateTime를 Server화일의 DateTime로 변경
              FHandle := FileOpen(gPath+FileName, fmOpenReadWrite);
              FileSetDate(FHandle, DateTimeToFileDate(sDate));
              FileClose(FHandle);
              Panel3.Caption := '';
              except on E:Exception do begin
                tMsg := '['+FileName+']';
              //ShowMessage(tMsg+' 파일받기를 완료하지 못했습니다!.');
              //ShowMessage(tMsg+' 파일받기를 완료하지 못했습니다!.'+ #13+ '구입처에 문의 하세요!. '+ #13 +E.Message);
              //Panel3.Caption := '파일받기를 실행할수 없습니다!.';
                Screen.Cursor := Save_Cursor;
                Exit;
              end;
            end;
            //ftp서버파일삭제
          //IdFTP1.Delete(FileName);
            ProgressBar1.Position := 0;
            Screen.Cursor := Save_Cursor;
            Panel3.Caption := '파일받기를 완료하였습니다!.';
            Application.ProcessMessages;
         end;
       //Label3.Caption:= '파일명 : ';
      //end;
      end;

    { for i := ListBox1.Items.Count - 1 downTo 0 do begin
         if (Pos('<DIR>',  ListBox1.Items[i]) > 0) or (CheckListBox1.Checked[i] = False) then
            Continue;
         FileName := Trim(Copy(ListBox1.Items[i], 40, 20));
         Label3.Caption:= '파일명 : ' + FileName;
         // Client File존재여부
         FHandle := FileOpen(gPath+FileName, fmOpenReadWrite);
         if FHandle > 0 then
         cDate := FileDateToDateTime(FileGetDate(FHandle)) else
         cDate := 0;

         FileClose(FHandle);
         //Server File DateTime저장
         Temp := Copy(ListBox1.Items[i], 1, 17);
         if Copy(Temp, 16, 2) = 'AM' then
            HH := Copy(Temp, 11, 2)
         else begin
            if StrToInt(Copy(Temp, 11, 2)) = 12 then
            HH := Copy(Temp, 11, 2) else
            HH := Format('%.02d',[StrToInt(Copy(Temp, 11, 2))+12]);
         end;

         if StrToInt(Copy(Temp,7,2)) < 80 then
         ServerDT := '20' + Copy(Temp, 7, 2) //YYYY
         else
         ServerDT := '19' + Copy(Temp, 7, 2); //YYYY
         ServerDt := ServerDt
                   + '-' + Copy(Temp, 1, 2)  //MM
                   + '-' + Copy(Temp, 4, 2)  //DD
                   + ' '
                   + HH                      //HH
                   + ':' + Copy(Temp, 14, 2) //MI
                   + ':00';                  //SS
         sDate := StrToDateTime(ServerDt);
       //Server화일이 Client화일보다 최신버전이면 DownLoad
         if(FHandle < 0) or (cDate < sDate)then begin
            try
              eMsg := '1';
              FCount2:=FCount2+1;
              Save_Cursor := Screen.Cursor;
              ProgressBar1.Position := 0;
              IdFTP1.TransferType := ftBinary;
              Screen.Cursor:= crHourGlass;
              Panel3.Caption := '파일을 받고 있습니다!.';
              BytesToTransfer := IdFTP1.Size(CheckListBox1.Items.Strings[i]);
              IdFTP1.Get(CheckListBox1.Items.Strings[i],CheckListBox1.Items.Strings[i],True);
            //IdFTP1.Put(gPath+FileName, FileName);

            //DownLoad완료후 Client화일의 DateTime를 Server화일의 DateTime로 변경
              FHandle := FileOpen(gPath+FileName, fmOpenReadWrite);
              FileSetDate(FHandle, DateTimeToFileDate(sDate));
              FileClose(FHandle);
              Panel3.Caption := '';
              except on E:Exception do begin
                tMsg := '['+FileName+']';
              //ShowMessage(tMsg+' 파일받기를 완료하지 못했습니다!.');
              //ShowMessage(tMsg+' 파일받기를 완료하지 못했습니다!.'+ #13+ '구입처에 문의 하세요!. '+ #13 +E.Message);
              //Panel3.Caption := '파일받기를 실행할수 없습니다!.';
                Screen.Cursor := Save_Cursor;
                Exit;
              end;
            end;
            ProgressBar1.Position := 0;
            Screen.Cursor := Save_Cursor;
            Panel3.Caption := '파일받기를 완료하였습니다!.';
         end;
       //Label3.Caption:= '파일명 : ';
      end; }

      if eMsg = '1' then begin
         FCount1:=FCount1+1;
         Label1.Caption:= IntToStr(FCount1);
         Label2.Caption:= IntToStr(FCount2);
         Sleep(1000);
      // ShellExecute(Application.Handle, nil, PChar(gPath+gExeFile), '', '', SW_SHOWNORMAL);
      end;
    { if Trim(gFile) <> '' then
         ShellExecute(Application.Handle, nil, PChar(gPath+gFile), '', '', SW_SHOWNORMAL);
      if(Application.MessageBox('다운로드 프로그램을 종료하고 '+#13+'프로그램을 실행 하시겠습니까?','확인', MB_OKCANCEL) = IDOK)then begin
         ShellExecute(Application.Handle, nil, PChar(gPath+gExeFile), '', '', SW_SHOWNORMAL);
         btnCloseClick(Self);
      end; }
      Panel3.Caption := 'FTP 서버 접속 중......';
   end
   else
      ShowMessage('호스트에 접속되어 있지 않습니다!.');

// Close;
end;

procedure TSeok90.Timer1Timer(Sender: TObject);
var i : Integer;
begin
  Timer1.Enabled:= False;
  try

  { /ifeaicompany
    /ifeaiitem
    /ifeaiinvtag      : 재고정보
    /ifeaircvresult   : 반입실적
    /ifeairetinresult : 입하실적
    /ifeaiso          : 출하예정
    /ifeaisoresult    : 출하실적 }

  { //-입하실적-//
    IdFTP1.Disconnect;
    hPath:=fPath+'/ifeaircvresult';

    Seok90.Refresh;
    if IdFTP1.Connected = True then
    ConnectToChck
    else
    ConnectToHost;
    for i := ListBox1.Items.Count - 1 downTo 0 do
      CheckListBox1.Checked[i] := True;
    btndownClick(Self);

    //-출하실적-//
    IdFTP1.Disconnect;
    hPath:=fPath+'/ifeaiso';

    Seok90.Refresh;
    if IdFTP1.Connected = True then
    ConnectToChck
    else
    ConnectToHost;
    for i := ListBox1.Items.Count - 1 downTo 0 do
      CheckListBox1.Checked[i] := True;
    btndownClick(Self);

    //-출하예정-//
    IdFTP1.Disconnect;
    hPath:=fPath+'/ifeaisoresult';

    Seok90.Refresh;
    if IdFTP1.Connected = True then
    ConnectToChck
    else
    ConnectToHost;
    for i := ListBox1.Items.Count - 1 downTo 0 do
      CheckListBox1.Checked[i] := True;
    btndownClick(Self);

    //-반입실적-//
    IdFTP1.Disconnect;
    hPath:=fPath+'/ifeaircvresult';

    Seok90.Refresh;
    if IdFTP1.Connected = True then
    ConnectToChck
    else
    ConnectToHost;
    for i := ListBox1.Items.Count - 1 downTo 0 do
      CheckListBox1.Checked[i] := True;
    btndownClick(Self);

    //-재고정보-//
    IdFTP1.Disconnect;
    hPath:=fPath+'/ifeaiinvtag';

    Seok90.Refresh;
    if IdFTP1.Connected = True then
    ConnectToChck
    else
    ConnectToHost;
    for i := ListBox1.Items.Count - 1 downTo 0 do
      CheckListBox1.Checked[i] := True;
    btndownClick(Self); }

    //-출고내역-//
    IdFTP1.Disconnect;
    hPath:=fPath;

    Seok90.Refresh;
    if IdFTP1.Connected = True then
    ConnectToChck
    else
    ConnectToHost;
    for i := ListBox1.Items.Count - 1 downTo 0 do
      CheckListBox1.Checked[i] := True;
    btndownClick(Self);

    ShowMessage('파일받기를 완료하였습니다!.');
    Close;
  finally
  Timer1.Enabled:= True;
  end;
end;

procedure TSeok90.FormShow(Sender: TObject);
var i : Integer;
begin
  FCount1:=0;
  FCount2:=0;
  Label1.Caption:= IntToStr(FCount1);
  Label2.Caption:= IntToStr(FCount2);
  btnConnectClick(Self);
//  for i := ListBox1.Items.Count - 1 downTo 0 do
//    CheckListBox1.Checked[i] := True;
end;

procedure TSeok90.FormCreate(Sender: TObject);
begin
  SetLocaleInfo(LOCALE_SYSTEM_DEFAULT, LOCALE_SLONGDATE, 'yyyy''년'' MM''월'' dd''일'' dddd');
  SetLocaleInfo(LOCALE_SYSTEM_DEFAULT, LOCALE_SSHORTDATE, 'yyyy-MM-dd');
  LongDateFormat := 'yyyy-MM-dd';
  ShortDateFormat := 'yyyy-MM-dd';

  SetLocaleInfo(LOCALE_SYSTEM_DEFAULT, LOCALE_STIMEFORMAT, 'HH:mm:ss');
  LongTimeFormat := 'HH:mm:ss';
  ShortTimeFormat := 'HH:mm:ss';
end;

procedure TSeok90.IdFTP1Work(Sender: TObject; AWorkMode: TWorkMode;
  const AWorkCount: Integer);
var
  S: String;
  TotalTime: TDateTime;
  H, M, Sec, MS: Word;
  DLTime: Double;
begin
  TotalTime :=  Now - STime;
  DecodeTime(TotalTime, H, M, Sec, MS);
  Sec := Sec + M * 60 + H * 3600;
  DLTime := Sec + MS / 1000;
  if DLTime > 0 then
    AverageSpeed := (AverageSpeed + (AWorkCount / 1024) / DLTime) / 2;

  S := FormatFloat('0.00 KB/s', AverageSpeed);
  ProgressBar1.Position := AWorkCount;
end;

procedure TSeok90.IdFTP1WorkBegin(Sender: TObject;
  AWorkMode: TWorkMode; const AWorkCountMax: Integer);
begin
  STime := Now;
  ProgressBar1.Max := BytesToTransfer;
  AverageSpeed := 0;
end;

procedure TSeok90.IdFTP1WorkEnd(Sender: TObject; AWorkMode: TWorkMode);
begin
  BytesToTransfer := 0;
  ProgressBar1.Position := 0;
  AverageSpeed := 0;
end;

end.
