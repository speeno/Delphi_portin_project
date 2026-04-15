unit Subu34_1;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, TFlatCheckBoxUnit,
  DBClient, DBGridEh, dxCore, dxButtons, ToolEdit, CornerButton;

type
  TSobo34_1 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel003: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    Panel101: TFlatPanel;
    Panel102: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Button101: TFlatButton;
    Button201: TFlatButton;
    Label101: TmyLabel3d;
    Label102: TmyLabel3d;
    Edit101: TFlatMaskEdit;
    Edit102: TFlatMaskEdit;
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    Edit106: TFlatEdit;
    CheckBox2: TFlatCheckBox;
    T3_Sub41: TClientDataSet;
    T3_Sub41GDATE: TStringField;
    T3_Sub41GUBUN: TStringField;
    T3_Sub41GCODE: TStringField;
    T3_Sub41GNAME: TStringField;
    T3_Sub41GIQUT: TFloatField;
    T3_Sub41GISUM: TFloatField;
    T3_Sub41GOQUT: TFloatField;
    T3_Sub41GOSUM: TFloatField;
    T3_Sub41GJQUT: TFloatField;
    T3_Sub41GJSUM: TFloatField;
    T3_Sub41GBQUT: TFloatField;
    T3_Sub41GBSUM: TFloatField;
    T3_Sub41GPQUT: TFloatField;
    T3_Sub41GPSUM: TFloatField;
    T3_Sub41GSUSU: TFloatField;
    T3_Sub41GSQUT: TFloatField;
    T3_Sub41GSSUM: TFloatField;
    T3_Sub41GSUMX: TFloatField;
    T3_Sub41GSUMY: TFloatField;
    T3_Sub42: TClientDataSet;
    T3_Sub42GDATE: TStringField;
    T3_Sub42GUBUN: TStringField;
    T3_Sub42GCODE: TStringField;
    T3_Sub42GNAME: TStringField;
    T3_Sub42GIQUT: TFloatField;
    T3_Sub42GISUM: TFloatField;
    T3_Sub42GOQUT: TFloatField;
    T3_Sub42GOSUM: TFloatField;
    T3_Sub42GJQUT: TFloatField;
    T3_Sub42GJSUM: TFloatField;
    T3_Sub42GBQUT: TFloatField;
    T3_Sub42GBSUM: TFloatField;
    T3_Sub42GPQUT: TFloatField;
    T3_Sub42GPSUM: TFloatField;
    T3_Sub42GSUSU: TFloatField;
    T3_Sub42GSQUT: TFloatField;
    T3_Sub42GSSUM: TFloatField;
    T3_Sub42GSUMX: TFloatField;
    T3_Sub42GSUMY: TFloatField;
    Label100: TmyLabel3d;
    Edit109: TFlatNumber;
    myLabel3d1: TmyLabel3d;
    Button703: TFlatButton;
    CornerButton1: TCornerButton;
    CornerButton2: TCornerButton;
    CornerButton3: TCornerButton;
    CornerButton9: TCornerButton;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label303: TmyLabel3d;
    Label309: TmyLabel3d;
    DateEdit1: TDateEdit;
    DateEdit2: TDateEdit;
    Button701: TFlatButton;
    Button702: TFlatButton;
    dxButton1: TdxButton;
    DBGrid101: TDBGridEh;
    DBGrid201: TDBGridEh;
    CheckBox1: TFlatCheckBox;
    Panel103: TFlatPanel;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Button700: TFlatButton;
    CheckBox3: TFlatCheckBox;
    procedure FormActivate(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure Button001Click(Sender: TObject);
    procedure Button002Click(Sender: TObject);
    procedure Button003Click(Sender: TObject);
    procedure Button004Click(Sender: TObject);
    procedure Button005Click(Sender: TObject);
    procedure Button006Click(Sender: TObject);
    procedure Button007Click(Sender: TObject);
    procedure Button008Click(Sender: TObject);
    procedure Button009Click(Sender: TObject);
    procedure Button010Click(Sender: TObject);
    procedure Button011Click(Sender: TObject);
    procedure Button012Click(Sender: TObject);
    procedure Button013Click(Sender: TObject);
    procedure Button014Click(Sender: TObject);
    procedure Button015Click(Sender: TObject);
    procedure Button016Click(Sender: TObject);
    procedure Button017Click(Sender: TObject);
    procedure Button018Click(Sender: TObject);
    procedure Button019Click(Sender: TObject);
    procedure Button020Click(Sender: TObject);
    procedure Button021Click(Sender: TObject);
    procedure Button022Click(Sender: TObject);
    procedure Button023Click(Sender: TObject);
    procedure Button024Click(Sender: TObject);
    procedure Button101Click(Sender: TObject);
    procedure Button102Click(Sender: TObject);
    procedure Button103Click(Sender: TObject);
    procedure Button201Click(Sender: TObject);
    procedure Edit101Change(Sender: TObject);
    procedure Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit111KeyPress(Sender: TObject; var Key: Char);
    procedure Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit114KeyPress(Sender: TObject; var Key: Char);
    procedure Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid201KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101TitleClick(Column: TColumnEh);
    procedure DBGrid201TitleClick(Column: TColumnEh);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit2ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button700Click(Sender: TObject);
    procedure Button701Click(Sender: TObject);
    procedure Button702Click(Sender: TObject);
    procedure Button703Click(Sender: TObject);
    procedure CheckBox3Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo34_1: TSobo34_1;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo34_1.FormActivate(Sender: TObject);
begin
  nForm:='34_1';
  nSqry:=T3_Sub41;
  mSqry:=T3_Sub42;
end;

procedure TSobo34_1.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo34_1.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo34_1:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo34_1.Button001Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end; }
end;

procedure TSobo34_1.Button002Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak20.ShowModal;
  end; }
end;

procedure TSobo34_1.Button003Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo34_1.Button004Click(Sender: TObject);
begin
{ Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
  if Panel102.Caption ='창고도서' Then begin
     Panel102.Caption:='도 서 명';
  end else
  if Panel102.Caption ='도 서 명' Then begin
     Panel102.Caption:='본사도서';
  end else
  if Panel102.Caption ='본사도서' Then begin
     Panel102.Caption:='창고도서';
  end; }
//Tong20.Chang_00_01('34');
  Edit101.SetFocus;
end;

procedure TSobo34_1.Button005Click(Sender: TObject);
begin
//Tong20.Chang_00_02('34');
end;

procedure TSobo34_1.Button006Click(Sender: TObject);
begin
{ T00:=1;
  Button201Click(Self); }
end;

procedure TSobo34_1.Button007Click(Sender: TObject);
begin
  T00:=0;
  Button201Click(Self);
end;

procedure TSobo34_1.Button008Click(Sender: TObject);
begin
//Tong20.Zoom_Int_01('34');
end;

procedure TSobo34_1.Button009Click(Sender: TObject);
begin
//Tong20.Zoom_Out_01('34');
end;

procedure TSobo34_1.Button010Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo34_1.Button011Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo34_1.Button012Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnY1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo34_1.Button013Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY1(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo34_1.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('34-01');
end;

procedure TSobo34_1.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('34-02');
end;

procedure TSobo34_1.Button016Click(Sender: TObject);
begin
  Tong40.print_34_05(Self);
end;

procedure TSobo34_1.Button017Click(Sender: TObject);
begin
  Tong40.print_34_06(Self);
end;

procedure TSobo34_1.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo34_1.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo34_1.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo34_1.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont3(DBGrid101,DBGrid201);
end;

procedure TSobo34_1.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo34_1.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo34_1.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo34_1.Button101Click(Sender: TObject);
begin
  Sqlen := 'Select Scode From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
  Translate(Sqlen, '@Gcode', Edit107.Text);
  if Base10.Seek_Name(Sqlen)<>'1' then
     Button102Click(Self)
  else
     Button103Click(Self);
end;

procedure TSobo34_1.Button102Click(Sender: TObject);
var St1,St2,St3,St4,St5,St6,St7: String;
    nSumX,nSumY: Double;
    _S1_Ssub,_Sg_Csum,_Sv_Ghng: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;
  DataSource2.Enabled:=False;

  if Panel102.Caption='도 서 명' Then St2:='B';
  if Panel102.Caption='본사도서' Then St2:='A';
  if Panel102.Caption='창고도서' Then St2:='B';

  Button101.Caption:='';
  St4:=''; St5:='';

  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
       '('+'Bdate'+' is '+'null'+')'+' and '+
       'Ocode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  St1:=St1+' and '+
       'Bcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Bcode'+'<='+#39+Edit105.Text+#39;

  {-S1_Ssub-}
  Sqlen :=
  'Select Bcode,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
  'From S1_Ssub Where '+D_Select+St1+
  'Group By Bcode,Scode,Gubun,Pubun ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  ProgressBar1.Max:=SGrid.RowCount-1;
  While SGrid.RowCount-1 > List1 do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 4,List1],0);
    T02:=StrToIntDef(SGrid.Cells[ 5,List1],0);

    St3:=SGrid.Cells[ 0,List1];
    St4:='';
    St5:='';
    St6:='';
    St7:='';
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit107.Text,St3]),[loCaseInsensitive])=true then begin
        St4:=Base10.G4_Book.FieldByName('Gname').AsString; //Gname
        St5:=Base10.G4_Book.FieldByName('Ocode').AsString; //Ocode
        St6:=Base10.G4_Book.FieldByName('Gubun').AsString; //Gubun
        St7:=Base10.G4_Book.FieldByName('Gdang').AsString; //Gdang
      end;

      if St4='' then begin
      Sqlen := 'Select Gname,Ocode,Gubun,Gdang From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gubun
        St7:=Base10.Socket.GetData(1, 4); //Gdang
      end;
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
      nSqry.FieldByName('Gsqut').AsString:=St7;
    end;

    nSqry.Edit;
    St3:=SGrid.Cells[ 2,List1];
    St4:=SGrid.Cells[ 3,List1];
    St5:=SGrid.Cells[ 1,List1];
    if St5='Y' Then begin
      if St4='이동' Then begin
        nSqry.FieldByName('Gpsum').AsFloat:=nSqry.FieldByName('Gpsum').AsFloat+T01;
      end else
      if St4='반품' Then begin
        nSqry.FieldByName('Gisum').AsFloat:=nSqry.FieldByName('Gisum').AsFloat+T01;
      end else
      if St3='입고' Then begin
        nSqry.FieldByName('Giqut').AsFloat:=nSqry.FieldByName('Giqut').AsFloat+T01;
      end;
    end else begin
      if St4='증정' Then begin
        nSqry.FieldByName('Gjqut').AsFloat:=nSqry.FieldByName('Gjqut').AsFloat+T01;
      end else
      if St3='출고' Then begin
        nSqry.FieldByName('Goqut').AsFloat:=nSqry.FieldByName('Goqut').AsFloat+T01;
      end else
      if St3='폐기' Then begin
        if(St4='비품')Then begin
          nSqry.FieldByName('Gpqut').AsFloat:=nSqry.FieldByName('Gpqut').AsFloat+T01;
          nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat+T01;
        end else begin
          nSqry.FieldByName('Gpqut').AsFloat:=nSqry.FieldByName('Gpqut').AsFloat+T01;
          nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat+T01;
        end;
      end else
      if(St4='비품')or(St4='폐기')Then begin
        if St5='X' Then begin
          if(St4='비품')Then begin
          nSqry.FieldByName('Gbqut').AsFloat:=nSqry.FieldByName('Gbqut').AsFloat+T01;
          nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat-T01;
          end;
          if(St4='폐기')Then begin
          nSqry.FieldByName('Gpqut').AsFloat:=nSqry.FieldByName('Gpqut').AsFloat+T01;
          end;
        end else begin
          if(St4='비품')Then begin
          nSqry.FieldByName('Gbqut').AsFloat:=nSqry.FieldByName('Gbqut').AsFloat+T01;
          nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat-T01;
          end;
          if(St4='폐기')Then begin
          nSqry.FieldByName('Gpqut').AsFloat:=nSqry.FieldByName('Gpqut').AsFloat+T01;
          nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat+T01;
          end;
        { if St5='Z' Then
        //nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat+T01;
          nSqry.FieldByName('Gpqut').AsFloat:=nSqry.FieldByName('Gpqut').AsFloat+T01;
          if St5='Z' Then
          nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat+T01; }
        end;
      end else
      if St3='반품' Then begin
        nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat-T01;
        nSqry.FieldByName('Gbqut').AsFloat:=nSqry.FieldByName('Gbqut').AsFloat+T01;
      end;
    end;
    nSqry.Post;
  end;


  //---------------유통반품재고-----------------//
  St1:='Bdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Bdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
       'Ocode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  St1:=St1+' and '+
       'Bcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Bcode'+'<='+#39+Edit105.Text+#39;

  {-S1_Ssub-}
  Sqlen :=
  'Select Bcode,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
  'From S1_Ssub Where '+D_Select+St1+
  'Group By Bcode,Scode,Gubun,Pubun ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  ProgressBar1.Max:=SGrid.RowCount-1;
  While SGrid.RowCount-1 > List1 do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 4,List1],0);
    T02:=StrToIntDef(SGrid.Cells[ 5,List1],0);

    St3:=SGrid.Cells[ 0,List1];
    St4:='';
    St5:='';
    St6:='';
    St7:='';
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit107.Text,St3]),[loCaseInsensitive])=true then begin
        St4:=Base10.G4_Book.FieldByName('Gname').AsString; //Gname
        St5:=Base10.G4_Book.FieldByName('Ocode').AsString; //Ocode
        St6:=Base10.G4_Book.FieldByName('Gubun').AsString; //Gubun
        St7:=Base10.G4_Book.FieldByName('Gdang').AsString; //Gdang
      end;

      if St4='' then begin
      Sqlen := 'Select Gname,Ocode,Gubun,Gdang From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gubun
        St7:=Base10.Socket.GetData(1, 4); //Gdang
      end;
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
      nSqry.FieldByName('Gsqut').AsString:=St7;
    end;

    nSqry.Edit;
    St3:=SGrid.Cells[ 2,List1];
    St4:=SGrid.Cells[ 3,List1];
    St5:=SGrid.Cells[ 1,List1];
    if St5='Y' Then begin
      if St4='반품' Then begin
        nSqry.FieldByName('Gisum').AsFloat:=nSqry.FieldByName('Gisum').AsFloat+T01;
      end else
      if St3='입고' Then begin
        nSqry.FieldByName('Giqut').AsFloat:=nSqry.FieldByName('Giqut').AsFloat+T01;
      end;
    end else begin
      if St4='증정' Then begin
        nSqry.FieldByName('Gjqut').AsFloat:=nSqry.FieldByName('Gjqut').AsFloat+T01;
      end else
      if St3='출고' Then begin
        nSqry.FieldByName('Goqut').AsFloat:=nSqry.FieldByName('Goqut').AsFloat+T01;
      end else
      if St3='폐기' Then begin
        if(St4='비품')Then begin
          nSqry.FieldByName('Gpqut').AsFloat:=nSqry.FieldByName('Gpqut').AsFloat+T01;
          nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat+T01;
        end else begin
          nSqry.FieldByName('Gpqut').AsFloat:=nSqry.FieldByName('Gpqut').AsFloat+T01;
          nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat+T01;
        end;
      end else
      if(St4='비품')or(St4='폐기')Then begin
        if St5='X' Then begin
          if(St4='비품')Then begin
          nSqry.FieldByName('Gbqut').AsFloat:=nSqry.FieldByName('Gbqut').AsFloat+T01;
          nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat-T01;
          end;
          if(St4='폐기')Then begin
          nSqry.FieldByName('Gpqut').AsFloat:=nSqry.FieldByName('Gpqut').AsFloat+T01;
          end;
        end else begin
          if(St4='비품')Then begin
          nSqry.FieldByName('Gbqut').AsFloat:=nSqry.FieldByName('Gbqut').AsFloat+T01;
          nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat-T01;
          end;
          if(St4='폐기')Then begin
          nSqry.FieldByName('Gpqut').AsFloat:=nSqry.FieldByName('Gpqut').AsFloat+T01;
          nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat+T01;
          end;
        { if St5='Z' Then
        //nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat+T01;
          nSqry.FieldByName('Gpqut').AsFloat:=nSqry.FieldByName('Gpqut').AsFloat+T01;
          if St5='Z' Then
          nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat+T01; }
        end;
      end else
      if St3='반품' Then begin
        nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat-T01;
        nSqry.FieldByName('Gbqut').AsFloat:=nSqry.FieldByName('Gbqut').AsFloat+T01;
      end;
    end;
    nSqry.Post;
  end;
  //---------------유통반품재고-----------------//


  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
      '(Scode'+' ='+#39+'B'+#39+' or '+'Scode'+' ='+#39+'D'+#39+')';
  //   'Scode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  St1:=St1+' and '+
       'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Gcode'+'<='+#39+Edit105.Text+#39;

  {-Sg_Csum-}
  Sqlen :=
  'Select Scode,Gcode,Sum(Gbsum)as Gbsum '+
  'From Sg_Csum Where '+D_Select+St1+
  'Group By Scode,Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 2,List1],0);

    St3:=SGrid.Cells[ 1,List1];
    St4:='';
    St5:='';
    St6:='';
    St7:='';
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit107.Text,St3]),[loCaseInsensitive])=true then begin
        St4:=Base10.G4_Book.FieldByName('Gname').AsString; //Gname
        St5:=Base10.G4_Book.FieldByName('Ocode').AsString; //Ocode
        St6:=Base10.G4_Book.FieldByName('Gubun').AsString; //Gubun
        St7:=Base10.G4_Book.FieldByName('Gdang').AsString; //Gdang
      end;

      if St4='' then begin
      Sqlen := 'Select Gname,Ocode,Gubun,Gdang From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gubun
        St7:=Base10.Socket.GetData(1, 4); //Gdang
      end;
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
      nSqry.FieldByName('Gsqut').AsString:=St7;
    end;

    nSqry.Edit;
    if SGrid.Cells[ 0,List1]='D' then begin
    nSqry.FieldByName('Gosum').AsFloat:=nSqry.FieldByName('Gosum').AsFloat+T01;
    nSqry.FieldByName('Gpsum').AsFloat:=nSqry.FieldByName('Gpsum').AsFloat+T01;
    end else
    nSqry.FieldByName('Gpsum').AsFloat:=nSqry.FieldByName('Gpsum').AsFloat+T01;
    nSqry.Post;
  end;

  {-Sv_Ghng-}
  Sqlen :='Select Max(Gdate)as Gdate From Sv_Ghng '+
          'Where '+D_Select+
          'Gdate < '+#39+Edit101.Text+#39+' and  '+
          'Hcode = '+#39+Edit107.Text+#39;
  St1:=Base10.Seek_Name(Sqlen);

  {-In_Ssub-}
  _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Edit101.Text+#39+' and '+
            'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
            'Ocode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  _S1_Ssub:=_S1_Ssub+' and '+
            'Bcode'+'>='+#39+Edit103.Text+#39+' and '+
            'Bcode'+'<='+#39+Edit105.Text+#39;

  _Sg_Csum:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Edit101.Text+#39+' and '+
            'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
           '(Scode'+' ='+#39+'B'+#39+' or '+'Scode'+' ='+#39+'D'+#39+')';
  //        'Scode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  _Sg_Csum:=_Sg_Csum+' and '+
            'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
            'Gcode'+'<='+#39+Edit105.Text+#39;

  _Sv_Ghng:='Gdate'+' ='+#39+St1+#39+' and '+
            'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
            'Scode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  _Sv_Ghng:=_Sv_Ghng+' and '+
            'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
            'Gcode'+'<='+#39+Edit105.Text+#39;

  Tong40._Sv_Ghng_(_S1_Ssub,_Sg_Csum,_Sv_Ghng);

  sSqry.First;
  ProgressBar1.Position:=0;
  ProgressBar1.Max:=sSqry.RecordCount;
  While sSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
    St3:=sSqry.FieldByName('Gcode').AsString;
    St4:='';
    St5:='';
    St6:='';
    St7:='';
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit107.Text,St3]),[loCaseInsensitive])=true then begin
        St4:=Base10.G4_Book.FieldByName('Gname').AsString; //Gname
        St5:=Base10.G4_Book.FieldByName('Ocode').AsString; //Ocode
        St6:=Base10.G4_Book.FieldByName('Gubun').AsString; //Gubun
        St7:=Base10.G4_Book.FieldByName('Gdang').AsString; //Gdang
      end;

      if St4='' then begin
      Sqlen := 'Select Gname,Ocode,Gubun,Gdang From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gubun
        St7:=Base10.Socket.GetData(1, 4); //Gdang
      end;
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
      nSqry.FieldByName('Gsqut').AsString:=St7;
    end;
    nSqry.Edit;
    nSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat;
    nSqry.FieldByName('GsumY').AsFloat:=sSqry.FieldByName('GsumX').AsFloat;
    nSqry.FieldByName('Gssum').AsFloat:=sSqry.FieldByName('Gbqut').AsFloat;
    nSqry.Post;
    sSqry.Next;
  end;
  Base10.SpaceDel(nSqry,'Gcode','Gname');

{ if ((Base10.Database.Database='chul_02_db') and (Hnnnn='1019')) or (CheckBox1.Checked=True) then begin
    Base10.G4_Book.First;
    While Base10.G4_Book.EOF=False do begin
      if nSqry.Locate('Gcode',Base10.G4_Book.FieldByName('Gcode').AsString,[loCaseInsensitive])=False then begin
        nSqry.Append;
        nSqry.FieldByName('Gcode').AsString:=Base10.G4_Book.FieldByName('Gcode').AsString;
        nSqry.FieldByName('Gname').AsString:=Base10.G4_Book.FieldByName('Gname').AsString;
        nSqry.FieldByName('Gdate').AsString:=Base10.G4_Book.FieldByName('Ocode').AsString;
        nSqry.FieldByName('Gubun').AsString:=Base10.G4_Book.FieldByName('Gubun').AsString;
        nSqry.FieldByName('Gsqut').AsFloat :=Base10.G4_Book.FieldByName('Gdang').AsFloat;
        nSqry.Post;
      end;
      Base10.G4_Book.Next;
    end;
  end; }

  nSqry.First;
  mSqry.First;
  While nSqry.EOF=False do begin

  //nSqry.FieldByName('Gjqut').AsFloat- nSqry.FieldByName('Gbqut').AsFloat+
    nSqry.Edit;
    nSqry.FieldByName('GsumY').AsFloat:=nSqry.FieldByName('GsumY').AsFloat+
    nSqry.FieldByName('Giqut').AsFloat- nSqry.FieldByName('Goqut').AsFloat-
    nSqry.FieldByName('Gjqut').AsFloat+ nSqry.FieldByName('Gisum').AsFloat+
    nSqry.FieldByName('Gbsum').AsFloat+ nSqry.FieldByName('Gpsum').AsFloat;
  //nSqry.FieldByName('Gbsum').AsFloat;

    if nSqry.FieldByName('Gosum').AsFloat<>0 then
    nSqry.FieldByName('GsumY').AsFloat:=nSqry.FieldByName('GsumY').AsFloat-
    nSqry.FieldByName('Gosum').AsFloat;

    nSqry.FieldByName('Gssum').AsFloat:=nSqry.FieldByName('Gssum').AsFloat-
    nSqry.FieldByName('Gisum').AsFloat+ nSqry.FieldByName('Gjsum').AsFloat+
    nSqry.FieldByName('Gosum').AsFloat;

    nSqry.FieldByName('Gosum').AsFloat:=
    nSqry.FieldByName('Gsqut').AsFloat*nSqry.FieldByName('GsumY').AsFloat*(Edit109.Value/100);

    nSqry.FieldByName('Gbsum').AsFloat:=
    nSqry.FieldByName('Gsqut').AsFloat*nSqry.FieldByName('Gssum').AsFloat*(Edit109.Value/100);

    if(CheckBox3.Checked=True)then begin
    nSqry.FieldByName('Gssum').AsFloat:=0;
    nSqry.FieldByName('Gbsum').AsFloat:=0;
    end;

  { Sqlen := 'Select Gpost From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    nSqry.FieldByName('Gpost').AsString:=Base10.Seek_Name(Sqlen); }

    if nBase='xXx' then
    nSqry.FieldByName('Gssum').AsString:='';
    if nBase='xXx' then
    nSqry.FieldByName('Gbsum').AsString:='';

    nSqry.FieldByName('Gjqut').AsFloat:=
    nSqry.FieldByName('GsumY').AsFloat+nSqry.FieldByName('Gssum').AsFloat;

    nSqry.FieldByName('Gjsum').AsFloat:=
    nSqry.FieldByName('Gosum').AsFloat+nSqry.FieldByName('Gbsum').AsFloat;

    nSqry.Post;

    St3:=nSqry.FieldByName('Gubun').AsString;
    St4:=nSqry.FieldByName('Gubun').AsString;

    if mSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      Sqlen := 'Select Gname From G4_Gbun Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      St4:=Base10.Seek_Name(Sqlen);

      mSqry.Append;
      mSqry.FieldByName('Gcode').AsString:=St3;
      mSqry.FieldByName('Gname').AsString:=St4;
    end;

    mSqry.Edit;
    mSqry.FieldByName('GsumX').AsFloat:=
    mSqry.FieldByName('GsumX').AsFloat+nSqry.FieldByName('GsumX').AsFloat;
    mSqry.FieldByName('Giqut').AsFloat:=
    mSqry.FieldByName('Giqut').AsFloat+nSqry.FieldByName('Giqut').AsFloat;
    mSqry.FieldByName('Gisum').AsFloat:=
    mSqry.FieldByName('Gisum').AsFloat+nSqry.FieldByName('Gisum').AsFloat;
    mSqry.FieldByName('Goqut').AsFloat:=
    mSqry.FieldByName('Goqut').AsFloat+nSqry.FieldByName('Goqut').AsFloat;
    mSqry.FieldByName('Gjqut').AsFloat:=
    mSqry.FieldByName('Gjqut').AsFloat+nSqry.FieldByName('Gjqut').AsFloat;
    mSqry.FieldByName('Gbqut').AsFloat:=
    mSqry.FieldByName('Gbqut').AsFloat+nSqry.FieldByName('Gbqut').AsFloat;
    mSqry.FieldByName('Gpqut').AsFloat:=
    mSqry.FieldByName('Gpqut').AsFloat+nSqry.FieldByName('Gpqut').AsFloat;
    mSqry.FieldByName('Gpsum').AsFloat:=
    mSqry.FieldByName('Gpsum').AsFloat+nSqry.FieldByName('Gpsum').AsFloat;
    mSqry.FieldByName('GsumY').AsFloat:=
    mSqry.FieldByName('GsumY').AsFloat+nSqry.FieldByName('GsumY').AsFloat;
    mSqry.FieldByName('Gssum').AsFloat:=
    mSqry.FieldByName('Gssum').AsFloat+nSqry.FieldByName('Gssum').AsFloat;

    mSqry.FieldByName('Gosum').AsFloat:=
    mSqry.FieldByName('Gosum').AsFloat+nSqry.FieldByName('Gosum').AsFloat;
    mSqry.FieldByName('Gbsum').AsFloat:=
    mSqry.FieldByName('Gbsum').AsFloat+nSqry.FieldByName('Gbsum').AsFloat;
    mSqry.FieldByName('Gjqut').AsFloat:=
    mSqry.FieldByName('Gjqut').AsFloat+nSqry.FieldByName('Gjqut').AsFloat;
    mSqry.FieldByName('Gjsum').AsFloat:=
    mSqry.FieldByName('Gjsum').AsFloat+nSqry.FieldByName('Gjsum').AsFloat;
    mSqry.Post;
    nSqry.Next;
  end;

  nSqry.IndexName := 'IDX'+'GCODE'+'DOWN';
  mSqry.IndexName := 'IDX'+'GCODE'+'DOWN';
  nSqry.First;
  mSqry.First;
{ Tong20.Srart_33_01(Self);
  Tong20.Srart_33_02(Self); }
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo34_1.Button103Click(Sender: TObject);
var St1,St2,St3,St4,St5,St6,St7: String;
    nSumX,nSumY: Double;
    _S1_Ssub,_Sg_Csum,_Sv_Ghng,_Sb_Csum: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;
  DataSource2.Enabled:=False;

  if Panel102.Caption='도 서 명' Then St2:='B';
  if Panel102.Caption='본사도서' Then St2:='A';
  if Panel102.Caption='창고도서' Then St2:='B';

  Button101.Caption:='';
  St4:=''; St5:='';

  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
       'Ocode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  St1:=St1+' and '+
       'Bcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Bcode'+'<='+#39+Edit105.Text+#39;

  {-S1_Ssub-}
  Sqlen :=
  'Select Bcode,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
  'From S1_Ssub Where '+D_Select+St1+
  'Group By Bcode,Scode,Gubun,Pubun ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  ProgressBar1.Max:=SGrid.RowCount-1;
  While SGrid.RowCount-1 > List1 do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 4,List1],0);
    T02:=StrToIntDef(SGrid.Cells[ 5,List1],0);

    St3:=SGrid.Cells[ 0,List1];
    St4:='';
    St5:='';
    St6:='';
    St7:='';
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit107.Text,St3]),[loCaseInsensitive])=true then begin
        St4:=Base10.G4_Book.FieldByName('Gname').AsString; //Gname
        St5:=Base10.G4_Book.FieldByName('Ocode').AsString; //Ocode
        St6:=Base10.G4_Book.FieldByName('Gubun').AsString; //Gubun
        St7:=Base10.G4_Book.FieldByName('Gdang').AsString; //Gdang
      end;

      if St4='' then begin
      Sqlen := 'Select Gname,Ocode,Gubun,Gdang From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gubun
        St7:=Base10.Socket.GetData(1, 4); //Gdang
      end;
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
      nSqry.FieldByName('Gdang').AsString:=St7;
    end;

    nSqry.Edit;
    St3:=SGrid.Cells[ 2,List1];
    St4:=SGrid.Cells[ 3,List1];
    St5:=SGrid.Cells[ 1,List1];
    if St5='Y' Then begin
      if St4='반품' Then begin
      //nSqry.FieldByName('Gisum').AsFloat:=nSqry.FieldByName('Gisum').AsFloat+T01;
      end else
      if St3='입고' Then begin
        nSqry.FieldByName('Giqut').AsFloat:=nSqry.FieldByName('Giqut').AsFloat+T01;
      end;
    end else begin
      if St4='증정' Then begin
        nSqry.FieldByName('Gjqut').AsFloat:=nSqry.FieldByName('Gjqut').AsFloat+T01;
      end else
      if St3='출고' Then begin
        nSqry.FieldByName('Goqut').AsFloat:=nSqry.FieldByName('Goqut').AsFloat+T01;
      end else
      if(St4='비품')or(St4='폐기')Then begin
        if St5='X' Then begin
          nSqry.FieldByName('Gbqut').AsFloat:=nSqry.FieldByName('Gbqut').AsFloat+T01;
        //nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat-T01;
        end else begin
        //if St5='Z' Then
        //nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat+T01;
          nSqry.FieldByName('Gpqut').AsFloat:=nSqry.FieldByName('Gpqut').AsFloat+T01;
        //if St5='Z' Then
        //nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat+T01;
        end;
      end else
      if St3='반품' Then begin
      //nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat-T01;
        nSqry.FieldByName('Gbqut').AsFloat:=nSqry.FieldByName('Gbqut').AsFloat+T01;
      end;
    end;
    nSqry.Post;
  end;

  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
      '(Scode'+' ='+#39+'B'+#39+' or '+'Scode'+' ='+#39+'D'+#39+')';
  //   'Scode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  St1:=St1+' and '+
       'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Gcode'+'<='+#39+Edit105.Text+#39;

  {-Sg_Csum-}
  Sqlen :=
  'Select Scode,Gcode,Sum(Gbsum)as Gbsum '+
  'From Sg_Csum Where '+D_Select+St1+
  'Group By Scode,Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 2,List1],0);

    St3:=SGrid.Cells[ 1,List1];
    St4:='';
    St5:='';
    St6:='';
    St7:='';
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit107.Text,St3]),[loCaseInsensitive])=true then begin
        St4:=Base10.G4_Book.FieldByName('Gname').AsString; //Gname
        St5:=Base10.G4_Book.FieldByName('Ocode').AsString; //Ocode
        St6:=Base10.G4_Book.FieldByName('Gubun').AsString; //Gubun
        St7:=Base10.G4_Book.FieldByName('Gdang').AsString; //Gdang
      end;

      if St4='' then begin
      Sqlen := 'Select Gname,Ocode,Gubun,Gdang From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gubun
        St7:=Base10.Socket.GetData(1, 4); //Gdang
      end;
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
      nSqry.FieldByName('Gdang').AsString:=St7;
    end;

    nSqry.Edit;
    if SGrid.Cells[ 0,List1]='D' then begin
    nSqry.FieldByName('Gosum').AsFloat:=nSqry.FieldByName('Gosum').AsFloat+T01;
    nSqry.FieldByName('Gpsum').AsFloat:=nSqry.FieldByName('Gpsum').AsFloat+T01;
    end else
    nSqry.FieldByName('Gpsum').AsFloat:=nSqry.FieldByName('Gpsum').AsFloat+T01;
    nSqry.Post;
  end;

  {-Sv_Ghng-}
  Sqlen :='Select Max(Gdate)as Gdate From Sv_Ghng '+
          'Where '+D_Select+
          'Gdate < '+#39+Edit101.Text+#39+' and  '+
          'Hcode = '+#39+Edit107.Text+#39;
  St1:=Base10.Seek_Name(Sqlen);

  {-In_Ssub-}
  _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Edit101.Text+#39+' and '+
            'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
            'Ocode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  _S1_Ssub:=_S1_Ssub+' and '+
            'Bcode'+'>='+#39+Edit103.Text+#39+' and '+
            'Bcode'+'<='+#39+Edit105.Text+#39;

  _Sg_Csum:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Edit101.Text+#39+' and '+
            'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
           '(Scode'+' ='+#39+'B'+#39+' or '+'Scode'+' ='+#39+'D'+#39+')';
  //        'Scode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  _Sg_Csum:=_Sg_Csum+' and '+
            'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
            'Gcode'+'<='+#39+Edit105.Text+#39;

  _Sv_Ghng:='Gdate'+' ='+#39+St1+#39+' and '+
            'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
            'Scode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  _Sv_Ghng:=_Sv_Ghng+' and '+
            'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
            'Gcode'+'<='+#39+Edit105.Text+#39;

  Tong40._Sv_Ghng_(_S1_Ssub,_Sg_Csum,_Sv_Ghng);

  sSqry.First;
  ProgressBar1.Position:=0;
  ProgressBar1.Max:=sSqry.RecordCount;
  While sSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
    St3:=sSqry.FieldByName('Gcode').AsString;
    St4:='';
    St5:='';
    St6:='';
    St7:='';
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit107.Text,St3]),[loCaseInsensitive])=true then begin
        St4:=Base10.G4_Book.FieldByName('Gname').AsString; //Gname
        St5:=Base10.G4_Book.FieldByName('Ocode').AsString; //Ocode
        St6:=Base10.G4_Book.FieldByName('Gubun').AsString; //Gubun
        St7:=Base10.G4_Book.FieldByName('Gdang').AsString; //Gdang
      end;

      if St4='' then begin
      Sqlen := 'Select Gname,Ocode,Gubun,Gdang From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gubun
        St7:=Base10.Socket.GetData(1, 4); //Gdang
      end;
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
      nSqry.FieldByName('Gdang').AsString:=St7;
    end;
    nSqry.Edit;
    nSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat;
    nSqry.FieldByName('GsumY').AsFloat:=sSqry.FieldByName('GsumX').AsFloat;
  //nSqry.FieldByName('Gssum').AsFloat:=sSqry.FieldByName('Gbqut').AsFloat;
    nSqry.Post;
    sSqry.Next;
  end;


  //---------------반품재고xx반품재고-----------------//
  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
       'Scode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  St1:=St1+' and '+
       'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Gcode'+'<='+#39+Edit105.Text+#39;

  {-Sb_Csum-}
  Sqlen := 'Select Gcode,Gubun,Gsqut From Sb_Csum Where '+D_Select+St1+
           ' Order By Gdate,Gcode';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  ProgressBar1.Max:=SGrid.RowCount-1;
  While SGrid.RowCount-1 > List1 do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 2,List1],0);
    St3:=SGrid.Cells[ 0,List1];
    St4:='';
    St5:='';
    St6:='';
    St7:='';

    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit107.Text,St3]),[loCaseInsensitive])=true then begin
        St4:=Base10.G4_Book.FieldByName('Gname').AsString; //Gname
        St5:=Base10.G4_Book.FieldByName('Ocode').AsString; //Ocode
        St6:=Base10.G4_Book.FieldByName('Gubun').AsString; //Gubun
        St7:=Base10.G4_Book.FieldByName('Gdang').AsString; //Gdang
      end;

      if St4='' then begin
      Sqlen := 'Select Gname,Ocode,Gubun,Gdang From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gubun
        St7:=Base10.Socket.GetData(1, 4); //Gdang
      end;
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
      nSqry.FieldByName('Gdang').AsString:=St7;
    end;

    nSqry.Edit;

    if SGrid.Cells[ 1,List1]='반품' then begin
      nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat+T01;
    end else
    if SGrid.Cells[ 1,List1]='입고' then begin
      nSqry.FieldByName('Gisum').AsFloat:=nSqry.FieldByName('Gisum').AsFloat+T01;
    end else
    if SGrid.Cells[ 1,List1]='재생' then begin
      nSqry.FieldByName('Gisum').AsFloat:=nSqry.FieldByName('Gisum').AsFloat+T01;
    end else
    if SGrid.Cells[ 1,List1]='폐기' then begin
      nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat-T01;
    end;

    nSqry.Post;
  end;

  {-Sv_Ghng-}
  Sqlen :='Select Max(Gdate)as Gdate From Sv_Ghng '+
          'Where '+D_Select+
          'Gdate < '+#39+Edit101.Text+#39+' and  '+
          'Hcode = '+#39+Edit107.Text+#39;
  St1:=Base10.Seek_Name(Sqlen);

  _Sb_Csum:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Edit101.Text+#39+' and '+
            'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
            'Scode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  _Sb_Csum:=_Sb_Csum+' and '+
            'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
            'Gcode'+'<='+#39+Edit105.Text+#39;

  _Sv_Ghng:='Gdate'+' ='+#39+St1+#39+' and '+
            'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
            'Scode'+' Like '+#39+'%'+St2+'%'+#39;
  if Edit105.Text<>'' Then
  _Sv_Ghng:=_Sv_Ghng+' and '+
            'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
            'Gcode'+'<='+#39+Edit105.Text+#39;

  Tong40._Sb_Ghng_(_Sb_Csum,_Sv_Ghng);

  sSqry.First;
  While sSqry.EOF=False do begin
    St3:=sSqry.FieldByName('Gcode').AsString;
    St4:='';
    St5:='';
    St6:='';
    St7:='';
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit107.Text,St3]),[loCaseInsensitive])=true then begin
        St4:=Base10.G4_Book.FieldByName('Gname').AsString; //Gname
        St5:=Base10.G4_Book.FieldByName('Ocode').AsString; //Ocode
        St6:=Base10.G4_Book.FieldByName('Gubun').AsString; //Gubun
        St7:=Base10.G4_Book.FieldByName('Gdang').AsString; //Gdang
      end;

      if St4='' then begin
      Sqlen := 'Select Gname,Ocode,Gubun,Gdang From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gubun
        St7:=Base10.Socket.GetData(1, 4); //Gdang
      end;
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
      nSqry.FieldByName('Gdang').AsString:=St7;
    end;
    nSqry.Edit;
    nSqry.FieldByName('GsumX').AsFloat:=
    nSqry.FieldByName('GsumX').AsFloat+ sSqry.FieldByName('GsumX').AsFloat;
    nSqry.FieldByName('GsumY').AsFloat:=
    nSqry.FieldByName('GsumY').AsFloat+ sSqry.FieldByName('GsumX').AsFloat;
    nSqry.FieldByName('Gssum').AsFloat:=
    nSqry.FieldByName('Gssum').AsFloat+ sSqry.FieldByName('Gbqut').AsFloat;
    nSqry.Post;
    sSqry.Next;
  end;
  //---------------반품재고xx반품재고-----------------//


  Base10.SpaceDel(nSqry,'Gcode','Gname');

  nSqry.First;
  mSqry.First;
  While nSqry.EOF=False do begin

  //nSqry.FieldByName('Gjqut').AsFloat- nSqry.FieldByName('Gbqut').AsFloat+
    nSqry.Edit;
    nSqry.FieldByName('GsumY').AsFloat:=nSqry.FieldByName('GsumY').AsFloat+
    nSqry.FieldByName('Giqut').AsFloat- nSqry.FieldByName('Goqut').AsFloat-
    nSqry.FieldByName('Gjqut').AsFloat+ nSqry.FieldByName('Gpsum').AsFloat+
    nSqry.FieldByName('Gisum').AsFloat;
  //nSqry.FieldByName('Gbsum').AsFloat;

    if nSqry.FieldByName('Gosum').AsFloat<>0 then
    nSqry.FieldByName('GsumY').AsFloat:=nSqry.FieldByName('GsumY').AsFloat-
    nSqry.FieldByName('Gosum').AsFloat;

    nSqry.FieldByName('Gssum').AsFloat:=nSqry.FieldByName('Gssum').AsFloat-
    nSqry.FieldByName('Gisum').AsFloat+ nSqry.FieldByName('Gbsum').AsFloat+
    nSqry.FieldByName('Gosum').AsFloat;

    nSqry.Post;

    St3:=nSqry.FieldByName('Gubun').AsString;
    St4:=nSqry.FieldByName('Gubun').AsString;

    if mSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      Sqlen := 'Select Gname From G4_Gbun Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      St4:=Base10.Seek_Name(Sqlen);

      mSqry.Append;
      mSqry.FieldByName('Gcode').AsString:=St3;
      mSqry.FieldByName('Gname').AsString:=St4;
    end;

    mSqry.Edit;
    mSqry.FieldByName('GsumX').AsFloat:=
    mSqry.FieldByName('GsumX').AsFloat+nSqry.FieldByName('GsumX').AsFloat;
    mSqry.FieldByName('Giqut').AsFloat:=
    mSqry.FieldByName('Giqut').AsFloat+nSqry.FieldByName('Giqut').AsFloat;
    mSqry.FieldByName('Gisum').AsFloat:=
    mSqry.FieldByName('Gisum').AsFloat+nSqry.FieldByName('Gisum').AsFloat;
    mSqry.FieldByName('Goqut').AsFloat:=
    mSqry.FieldByName('Goqut').AsFloat+nSqry.FieldByName('Goqut').AsFloat;
    mSqry.FieldByName('Gjqut').AsFloat:=
    mSqry.FieldByName('Gjqut').AsFloat+nSqry.FieldByName('Gjqut').AsFloat;
    mSqry.FieldByName('Gbqut').AsFloat:=
    mSqry.FieldByName('Gbqut').AsFloat+nSqry.FieldByName('Gbqut').AsFloat;
    mSqry.FieldByName('Gpqut').AsFloat:=
    mSqry.FieldByName('Gpqut').AsFloat+nSqry.FieldByName('Gpqut').AsFloat;
    mSqry.FieldByName('Gpsum').AsFloat:=
    mSqry.FieldByName('Gpsum').AsFloat+nSqry.FieldByName('Gpsum').AsFloat;
    mSqry.FieldByName('GsumY').AsFloat:=
    mSqry.FieldByName('GsumY').AsFloat+nSqry.FieldByName('GsumY').AsFloat;
    mSqry.FieldByName('Gssum').AsFloat:=
    mSqry.FieldByName('Gssum').AsFloat+nSqry.FieldByName('Gssum').AsFloat;
    mSqry.Post;
    nSqry.Next;
  end;

  nSqry.IndexName := 'IDX'+'GCODE'+'DOWN';
  mSqry.IndexName := 'IDX'+'GCODE'+'DOWN';
  nSqry.First;
  mSqry.First;
  Tong20.Srart_33_01(Self);
  Tong20.Srart_33_02(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo34_1.Button201Click(Sender: TObject);
var St1: String;
begin
  Refresh;
  if(T00=0)Then begin
    Button101.Caption:=mSqry.FieldByName('Gname').AsString;
    St1:='Gubun'+'='+#39+mSqry.FieldByName('Gcode').AsString+#39;
    nSqry.Filter:=St1;
    nSqry.Filtered:=True;
  end;
  if(T00=1)Then begin
    Button101.Caption:='';
    nSqry.Filtered:=False;
  end;
end;

procedure TSobo34_1.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit102.Focused=True)and(Edit102.SelStart=10)and(Length(Trim(Edit102.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit104.Focused=True)and(Edit104.SelStart=80)and(Length(Trim(Edit104.Text))=80))or
    ((Edit106.Focused=True)and(Edit106.SelStart=80)and(Length(Trim(Edit106.Text))=80))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo34_1.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo34_1.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo34_1.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo34_1.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo34_1.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
  if Edit108.Focused=True Then begin
       Edit107.Text:='';
    if Edit108.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit108.Text;
    Seak80.FilterTing(Edit108.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end;
  end else
  if(Edit104.Focused=True)Then begin
       Edit103.Text:='';
    if Edit104.Text<>'' Then begin
    Seek40.Edit1.Text:=Edit104.Text;
    Seek40.FilterTing(Edit104.Text,Edit107.Text);
    if Seek40.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seek40.Query1Gcode.AsString;
      Edit104.Text:=Seek40.Query1Gname.AsString;
    end else
    if Seek40.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seek40.Query1Gcode.AsString;
      Edit104.Text:=Seek40.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if(Edit106.Focused=True)Then begin
       Edit105.Text:='';
    if Edit106.Text<>'' Then begin
    Seek40.Edit1.Text:=Edit106.Text;
    Seek40.FilterTing(Edit106.Text,Edit107.Text);
    if Seek40.Query1.RecordCount=1 Then begin
      Edit105.Text:=Seek40.Query1Gcode.AsString;
      Edit106.Text:=Seek40.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seek40.ShowModal=mrOK Then begin
      Edit105.Text:=Seek40.Query1Gcode.AsString;
      Edit106.Text:=Seek40.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else
      Button101Click(Self);
  end;
  end;
end;

procedure TSobo34_1.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo34_1.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo34_1.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if mSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo34_1.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo34_1.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if nSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  if Key=VK_F2 Then Tong40.Print_56_01(Self);
  if Key=VK_F3 Then Tong40.Print_56_02(Self);
  end;
end;

procedure TSobo34_1.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(mSqry,Column);
end;

procedure TSobo34_1.DBGrid201TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo34_1.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo34_1.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo34_1.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo34_1.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo34_1.DateEdit2ButtonClick(Sender: TObject);
begin
  DateEdit2.Date :=StrToDate(Edit102.Text);
end;

procedure TSobo34_1.DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit102.Text :=DateToStr(ADate);
end;

procedure TSobo34_1.Button700Click(Sender: TObject);
begin
  Seak80.Edit1.Text:=Edit108.Text;
  if Edit108.Text='' then
  Seak80.FilterTing('') else
  Seak80.FilterTing(Edit108.Text);
  if Seak80.Query1.RecordCount=1 Then begin
    Edit107.Text:=Seak80.Query1Gcode.AsString;
    Edit108.Text:=Seak80.Query1Gname.AsString;
  end else
  if Seak80.ShowModal=mrOK Then begin
    Edit107.Text:=Seak80.Query1Gcode.AsString;
    Edit108.Text:=Seak80.Query1Gname.AsString;
  end;
end;

procedure TSobo34_1.Button701Click(Sender: TObject);
begin
  Seek40.Edit1.Text:=Edit104.Text;
  if Edit104.Text='' then
  Seek40.FilterTing('',Edit107.Text) else
  Seek40.FilterTing(Edit104.Text,Edit107.Text);
  if Seek40.Query1.RecordCount=1 Then begin
    Edit103.Text:=Seek40.Query1Gcode.AsString;
    Edit104.Text:=Seek40.Query1Gname.AsString;
  end else
  if Seek40.ShowModal=mrOK Then begin
    Edit103.Text:=Seek40.Query1Gcode.AsString;
    Edit104.Text:=Seek40.Query1Gname.AsString;
  end;
end;

procedure TSobo34_1.Button702Click(Sender: TObject);
begin
  Seek40.Edit1.Text:=Edit106.Text;
  if Edit106.Text='' then
  Seek40.FilterTing('',Edit107.Text) else
  Seek40.FilterTing(Edit106.Text,Edit107.Text);
  if Seek40.Query1.RecordCount=1 Then begin
    Edit105.Text:=Seek40.Query1Gcode.AsString;
    Edit106.Text:=Seek40.Query1Gname.AsString;
  end else
  if Seek40.ShowModal=mrOK Then begin
    Edit105.Text:=Seek40.Query1Gcode.AsString;
    Edit106.Text:=Seek40.Query1Gname.AsString;
  end;
end;

procedure TSobo34_1.Button703Click(Sender: TObject);
var St3,St4: String;
begin
  if nSqry.Active=True Then begin
  Base10.OpenShow(mSqry);
  nSqry.First;
  mSqry.First;
  While nSqry.EOF=False do begin

    nSqry.Edit;

    nSqry.FieldByName('Gosum').AsFloat:=
    nSqry.FieldByName('Gsqut').AsFloat*nSqry.FieldByName('GsumY').AsFloat*(Edit109.Value/100);

    nSqry.FieldByName('Gbsum').AsFloat:=
    nSqry.FieldByName('Gsqut').AsFloat*nSqry.FieldByName('Gssum').AsFloat*(Edit109.Value/100);

    nSqry.FieldByName('Gjqut').AsFloat:=
    nSqry.FieldByName('GsumY').AsFloat+nSqry.FieldByName('Gssum').AsFloat;

    nSqry.FieldByName('Gjsum').AsFloat:=
    nSqry.FieldByName('Gosum').AsFloat+nSqry.FieldByName('Gbsum').AsFloat;


    St3:=nSqry.FieldByName('Gubun').AsString;
    St4:=nSqry.FieldByName('Gubun').AsString;

    nSqry.Post;

    if mSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      Sqlen := 'Select Gname From G4_Gbun Where '+D_Select+'Hcode=''@Hcode'' and Gcode=''@Gcode''';
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Translate(Sqlen, '@Gcode', St3);
      St4:=Base10.Seek_Name(Sqlen);

      mSqry.Append;
      mSqry.FieldByName('Gcode').AsString:=St3;
      mSqry.FieldByName('Gname').AsString:=St4;
    end;

    mSqry.Edit;
    mSqry.FieldByName('GsumX').AsFloat:=
    mSqry.FieldByName('GsumX').AsFloat+nSqry.FieldByName('GsumX').AsFloat;
    mSqry.FieldByName('Giqut').AsFloat:=
    mSqry.FieldByName('Giqut').AsFloat+nSqry.FieldByName('Giqut').AsFloat;
    mSqry.FieldByName('Gisum').AsFloat:=
    mSqry.FieldByName('Gisum').AsFloat+nSqry.FieldByName('Gisum').AsFloat;
    mSqry.FieldByName('Goqut').AsFloat:=
    mSqry.FieldByName('Goqut').AsFloat+nSqry.FieldByName('Goqut').AsFloat;
    mSqry.FieldByName('Gjqut').AsFloat:=
    mSqry.FieldByName('Gjqut').AsFloat+nSqry.FieldByName('Gjqut').AsFloat;
    mSqry.FieldByName('Gbqut').AsFloat:=
    mSqry.FieldByName('Gbqut').AsFloat+nSqry.FieldByName('Gbqut').AsFloat;
    mSqry.FieldByName('Gpqut').AsFloat:=
    mSqry.FieldByName('Gpqut').AsFloat+nSqry.FieldByName('Gpqut').AsFloat;
    mSqry.FieldByName('Gpsum').AsFloat:=
    mSqry.FieldByName('Gpsum').AsFloat+nSqry.FieldByName('Gpsum').AsFloat;
    mSqry.FieldByName('GsumY').AsFloat:=
    mSqry.FieldByName('GsumY').AsFloat+nSqry.FieldByName('GsumY').AsFloat;
    mSqry.FieldByName('Gssum').AsFloat:=
    mSqry.FieldByName('Gssum').AsFloat+nSqry.FieldByName('Gssum').AsFloat;

    mSqry.FieldByName('Gosum').AsFloat:=
    mSqry.FieldByName('Gosum').AsFloat+nSqry.FieldByName('Gosum').AsFloat;
    mSqry.FieldByName('Gbsum').AsFloat:=
    mSqry.FieldByName('Gbsum').AsFloat+nSqry.FieldByName('Gbsum').AsFloat;
    mSqry.FieldByName('Gjqut').AsFloat:=
    mSqry.FieldByName('Gjqut').AsFloat+nSqry.FieldByName('Gjqut').AsFloat;
    mSqry.FieldByName('Gjsum').AsFloat:=
    mSqry.FieldByName('Gjsum').AsFloat+nSqry.FieldByName('Gjsum').AsFloat;
    mSqry.Post;
    nSqry.Next;
  end;
  end;
end;

procedure TSobo34_1.CheckBox3Click(Sender: TObject);
var St3,St4: String;
begin
  if nSqry.Active=True Then begin
  Base10.OpenShow(mSqry);
  nSqry.First;
  mSqry.First;
  While nSqry.EOF=False do begin

    nSqry.Edit;

    nSqry.FieldByName('Gosum').AsFloat:=
    nSqry.FieldByName('Gsqut').AsFloat*nSqry.FieldByName('GsumY').AsFloat*(Edit109.Value/100);

    nSqry.FieldByName('Gbsum').AsFloat:=
    nSqry.FieldByName('Gsqut').AsFloat*nSqry.FieldByName('Gssum').AsFloat*(Edit109.Value/100);

    nSqry.FieldByName('Gssum').AsFloat:=0;
    nSqry.FieldByName('Gbsum').AsFloat:=0;

    nSqry.FieldByName('Gjqut').AsFloat:=
    nSqry.FieldByName('GsumY').AsFloat+nSqry.FieldByName('Gssum').AsFloat;

    nSqry.FieldByName('Gjsum').AsFloat:=
    nSqry.FieldByName('Gosum').AsFloat+nSqry.FieldByName('Gbsum').AsFloat;


    St3:=nSqry.FieldByName('Gubun').AsString;
    St4:=nSqry.FieldByName('Gubun').AsString;

    nSqry.Post;

    if mSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      Sqlen := 'Select Gname From G4_Gbun Where '+D_Select+'Hcode=''@Hcode'' and Gcode=''@Gcode''';
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Translate(Sqlen, '@Gcode', St3);
      St4:=Base10.Seek_Name(Sqlen);

      mSqry.Append;
      mSqry.FieldByName('Gcode').AsString:=St3;
      mSqry.FieldByName('Gname').AsString:=St4;
    end;

    mSqry.Edit;
    mSqry.FieldByName('GsumX').AsFloat:=
    mSqry.FieldByName('GsumX').AsFloat+nSqry.FieldByName('GsumX').AsFloat;
    mSqry.FieldByName('Giqut').AsFloat:=
    mSqry.FieldByName('Giqut').AsFloat+nSqry.FieldByName('Giqut').AsFloat;
    mSqry.FieldByName('Gisum').AsFloat:=
    mSqry.FieldByName('Gisum').AsFloat+nSqry.FieldByName('Gisum').AsFloat;
    mSqry.FieldByName('Goqut').AsFloat:=
    mSqry.FieldByName('Goqut').AsFloat+nSqry.FieldByName('Goqut').AsFloat;
    mSqry.FieldByName('Gjqut').AsFloat:=
    mSqry.FieldByName('Gjqut').AsFloat+nSqry.FieldByName('Gjqut').AsFloat;
    mSqry.FieldByName('Gbqut').AsFloat:=
    mSqry.FieldByName('Gbqut').AsFloat+nSqry.FieldByName('Gbqut').AsFloat;
    mSqry.FieldByName('Gpqut').AsFloat:=
    mSqry.FieldByName('Gpqut').AsFloat+nSqry.FieldByName('Gpqut').AsFloat;
    mSqry.FieldByName('Gpsum').AsFloat:=
    mSqry.FieldByName('Gpsum').AsFloat+nSqry.FieldByName('Gpsum').AsFloat;
    mSqry.FieldByName('GsumY').AsFloat:=
    mSqry.FieldByName('GsumY').AsFloat+nSqry.FieldByName('GsumY').AsFloat;
    mSqry.FieldByName('Gssum').AsFloat:=
    mSqry.FieldByName('Gssum').AsFloat+nSqry.FieldByName('Gssum').AsFloat;

    mSqry.FieldByName('Gosum').AsFloat:=
    mSqry.FieldByName('Gosum').AsFloat+nSqry.FieldByName('Gosum').AsFloat;
    mSqry.FieldByName('Gbsum').AsFloat:=
    mSqry.FieldByName('Gbsum').AsFloat+nSqry.FieldByName('Gbsum').AsFloat;
    mSqry.FieldByName('Gjqut').AsFloat:=
    mSqry.FieldByName('Gjqut').AsFloat+nSqry.FieldByName('Gjqut').AsFloat;
    mSqry.FieldByName('Gjsum').AsFloat:=
    mSqry.FieldByName('Gjsum').AsFloat+nSqry.FieldByName('Gjsum').AsFloat;
    mSqry.Post;
    nSqry.Next;
  end;
  end;
end;

end.
