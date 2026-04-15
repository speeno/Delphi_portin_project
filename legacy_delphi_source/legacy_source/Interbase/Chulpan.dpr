program Chulpan;

uses
  Forms,
  Controls,
  Dialogs,
  Chul in 'Chul.pas' {Subu00},
  Base01 in 'Base01.pas' {Base10: TDataModule},
  Seak01 in '..\Seak01.pas' {Seak10},
  Seak02 in '..\Seak02.pas' {Seak20},
  Seak03 in '..\Seak03.pas' {Seak30},
  Seak04 in '..\Seak04.pas' {Seak40},
  Seak05 in '..\Seak05.pas' {Seak50},
  Seak06 in '..\Seak06.pas' {Seak60},
  Seak07 in '..\Seak07.pas' {Seak70},
  Seak08 in '..\Seak08.pas' {Seak80},
  Seak09 in '..\Seak09.pas' {Seak90},
  Seek01 in 'Seek01.pas' {Seek10},
  Seek02 in 'Seek02.pas' {Seek20},
  Seek03 in 'Seek03.pas' {Seek30},
  Seek04 in 'Seek04.pas' {Seek40},
  Seek05 in 'Seek05.pas' {Seek50},
  Seek06 in 'Seek06.pas' {Seek60},
  Seek07 in 'Seek07.pas' {Seek70},
  Seek08 in 'Seek08.pas' {Seek80},
  Seek09 in 'Seek09.pas' {Seek90},
  Seok01 in '..\Seok01.pas' {Seok10},
  Seok02 in '..\Seok02.pas' {Seok20},
  Seok03 in '..\Seok03.pas' {Seok30},
  Subu10 in '..\Subu10.pas' {Sobo10},
  Subu11 in '..\Subu11.pas' {Sobo11},
  Subu12 in '..\Subu12.pas' {Sobo12},
  Subu13 in '..\Subu13.pas' {Sobo13},
  Subu14 in '..\Subu14.pas' {Sobo14},
  Subu15 in '..\Subu15.pas' {Sobo15},
  Subu16 in '..\Subu16.pas' {Sobo16},
  Subu17 in 'Subu17.pas' {Sobo17},
  Subu18 in '..\Subu18.pas' {Sobo18},
  Subu19 in '..\Subu19.pas' {Sobo19},
  Subu20 in '..\Subu20.pas' {Sobo20},
  Subu21 in 'Subu21.pas' {Sobo21},
  Subu22 in '..\Subu22.pas' {Sobo22},
  Subu23 in '..\Subu23.pas' {Sobo23},
  Subu24 in '..\Subu24.pas' {Sobo24},
  Subu25 in '..\Subu25.pas' {Sobo25},
  Subu26 in '..\Subu26.pas' {Sobo26},
  Subu27 in '..\Subu27.pas' {Sobo27},
  Subu28 in '..\Subu28.pas' {Sobo28},
  Subu29 in '..\Subu29.pas' {Sobo29},
  Subu30 in '..\Subu30.pas' {Sobo30},
  Subu31 in '..\Subu31.pas' {Sobo31},
  Subu32 in '..\Subu32.pas' {Sobo32},
  Subu33 in '..\Subu33.pas' {Sobo33},
  Subu34 in '..\Subu34.pas' {Sobo34},
  Subu35 in '..\Subu35.pas' {Sobo35},
  Subu36 in '..\Subu36.pas' {Sobo36},
  Subu37 in '..\Subu37.pas' {Sobo37},
  Subu38 in '..\Subu38.pas' {Sobo38},
  Subu39 in '..\Subu39.pas' {Sobo39},
  Subu40 in '..\Subu40.pas' {Sobo40},
  Subu41 in '..\Subu41.pas' {Sobo41},
  Subu42 in '..\Subu42.pas' {Sobo42},
  Subu43 in '..\Subu43.pas' {Sobo43},
  Subu44 in '..\Subu44.pas' {Sobo44},
  Subu45 in 'Subu45.pas' {Sobo45},
  Subu46 in '..\Subu46.pas' {Sobo46},
  Subu47 in '..\Subu47.pas' {Sobo47},
  Subu48 in '..\Subu48.pas' {Sobo48},
  Subu49 in '..\Subu49.pas' {Sobo49},
  Subu50 in '..\Subu50.pas' {Sobo50},
  Subu51 in 'Subu51.pas' {Sobo51},
  Subu52 in '..\Subu52.pas' {Sobo52},
  Subu53 in 'Subu53.pas' {Sobo53},
  Subu54 in 'Subu54.pas' {Sobo54},
  Subu55 in 'Subu55.pas' {Sobo55},
  Subu56 in 'Subu56.pas' {Sobo56},
  Subu57 in 'Subu57.pas' {Sobo57},
  Subu58 in 'Subu58.pas' {Sobo58},
  Subu59 in '..\Subu59.pas' {Sobo59},
  Subu60 in '..\Subu60.pas' {Sobo60},
  Subu61 in '..\Subu61.pas' {Sobo61},
  Subu62 in '..\Subu62.pas' {Sobo62},
  Subu63 in '..\Subu63.pas' {Sobo63},
  Subu64 in '..\Subu64.pas' {Sobo64},
  Subu65 in '..\.\Data\Subu65.pas' {Sobo65},
  Subu66 in '..\.\Data\Subu66.pas' {Sobo66},
  Subu67 in '..\Subu67.pas' {Sobo67},
  Subu68 in '..\Subu68.pas' {Sobo68},
  Subu69 in '..\Subu69.pas' {Sobo69},
  Subu71 in '..\Subu71.pas' {Sobo71},
  Seep11 in '..\Seep11.pas' {Seen11},
  Seep13 in '..\Seep13.pas' {Seen13},
  Tong01 in '..\Tong01.pas' {Tong10},
  Tong02 in '..\Tong02.pas' {Tong20},
  Tong03 in '..\Tong03.pas' {Tong30},
  Tong04 in 'Tong04.pas' {Tong40},
  Tong05 in '..\Tong05.pas' {Tong50},
  Tong06 in '..\Tong06.pas' {Tong60},
  Tong07 in '..\Tong07.pas' {Tong70: TFrame},
  Tong08 in '..\Tong08.pas' {Tong80};

{$R *.RES}

begin
  Application.Initialize;
  Sobo10 := TSobo10.Create(Application);
  if Sobo10.ShowModal = mrOK then begin
  Sobo10.Free;
  Application.CreateForm(TSubu00, Subu00);
  Application.CreateForm(TBase10, Base10);
  Application.CreateForm(TSeak10, Seak10);
  Application.CreateForm(TSeak20, Seak20);
  Application.CreateForm(TSeak30, Seak30);
  Application.CreateForm(TSeak40, Seak40);
  Application.CreateForm(TSeak50, Seak50);
  Application.CreateForm(TSeak60, Seak60);
  Application.CreateForm(TSeak70, Seak70);
  Application.CreateForm(TSeak80, Seak80);
  Application.CreateForm(TSeak90, Seak90);
  Application.CreateForm(TSeek10, Seek10);
  Application.CreateForm(TSeek20, Seek20);
  Application.CreateForm(TSeek30, Seek30);
  Application.CreateForm(TSeek40, Seek40);
  Application.CreateForm(TSeek50, Seek50);
  Application.CreateForm(TSeek60, Seek60);
  Application.CreateForm(TSeek70, Seek70);
  Application.CreateForm(TSeek80, Seek80);
  Application.CreateForm(TSeek90, Seek90);
  Application.CreateForm(TSeok10, Seok10);
  Application.CreateForm(TSeok20, Seok20);
  Application.CreateForm(TTong20, Tong20);
  Application.CreateForm(TTong30, Tong30);
  Application.CreateForm(TTong40, Tong40);
  Application.CreateForm(TTong60, Tong60);
  Application.CreateForm(TTong80, Tong80);
  Application.CreateForm(TSobo71, Sobo71);
  Application.Run;
  end
  else
  MessageDlg('로그인 실패... '+#13+'프로그램을 종료합니다.', mtError, [mbOK], 0);
end.
