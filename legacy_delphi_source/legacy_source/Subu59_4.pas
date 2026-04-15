unit Subu59_4;
//물표출력을 위한 unit.

interface

uses StdCtrls, SysUtils;

type
  TCls_Mulpyo_Happyday = class
  private
    printer_name: string;

    uX,//좌표 x
    uY,//좌표 y
    uHeight,//font size
    uAngle,//회전 각도
    uBold,//style
    uUnderline: integer;//밑줄
    uFont_name,//font name
    uContent_1,
    uContent_2: string;//출력내용
    uCommand: string;
    uLine_width,//bar 출력시 width
    uLine_height: integer;//bar 출력시 height
  public
    constructor Create();

    procedure command_open;
    procedure command_close;
    procedure print_contents(fDate, fCust_name, fQty, fBunch, fPublisher: string);
    // ============ title 부분 출력
    procedure print_title_date;// 날짜(title)
    procedure print_title_company;// 물류사(title)
    procedure print_title_qty;// 수량(title)
    procedure print_title_bunch;// 덩이(title)
    // ============ content 부분 출력
    procedure Set_contents(fContent: string);

    procedure print_content_date(fDate: string);//날짜(content)
    procedure print_content_company;//물류사(content)
    procedure print_content_cust(fCust_name: string);//거래처(content)
    procedure print_content_qty(fQty: string);//수량(content)
    procedure print_content_bunch(fBunch: string);//덩이(content)
    procedure print_content_publisher(fPublisher: string);//출판사(content)
    // ============ 가로선 출력
    procedure print_line_hor_1;
    procedure print_line_hor_2;
    procedure print_line_hor_3;
    procedure print_line_hor_4;
    // ============ 세로선 출력
    procedure print_line_ver_1;
    procedure print_line_ver_2;
    procedure print_line_ver_3;
    procedure print_line_ver_4;
    procedure print_line_ver_5;
    procedure print_line_ver_6;
    procedure print_line_ver_7;
    procedure print_line_ver_8;
    procedure print_line_ver_9;
  end;

  procedure openport(PrinterName: PChar); stdcall; far; external 'tsclib.dll';
  procedure closeport; external 'tsclib.dll';
  procedure sendcommand(Command: PChar); stdcall; far; external 'tsclib.dll';
  procedure barcode(X, Y, CodeType, Height, Readable, Rotation, Narrow, Wide, Code: PChar); stdcall; far; external 'tsclib.dll';
  procedure clearbuffer; external 'tsclib.dll';
  procedure printlabel(NumberOfSet, NumberOfCopy: PChar); stdcall; far; external 'tsclib.dll';
  procedure windowsfont(X, Y, FontHeight, Rotation, FontStyle, FontUnderline: integer;
                FaceName, TextContent: PChar); stdcall; far; external 'tsclib.dll';

implementation

constructor TCls_Mulpyo_Happyday.Create();
begin
  printer_name := 'TSC DA220';
end;

procedure TCls_Mulpyo_Happyday.print_title_date;// 날짜(title)
begin
  uX := 28;
  uY := 32;
  uHeight := 35;
  uBold := 0;
  uAngle := 0;
  uUnderline := 0;
  uFont_name := 'Arial';
  uContent_1 := '날짜';

  windowsfont(uX, uY, uHeight, uAngle, uBold, uUnderline, pChar(uFont_name), pChar(uContent_1));
end;

procedure TCls_Mulpyo_Happyday.print_title_company;// 물류사(title)
begin
  uX := 326;
  uY := 32;
  uHeight := 35;
  uBold := 0;
  uAngle := 0;
  uUnderline := 0;
  uFont_name := 'Arial';
  uContent_1 := '물류';

  windowsfont(uX, uY, uHeight, uAngle, uBold, uUnderline, pChar(uFont_name), pchar(uContent_1));
end;

procedure TCls_Mulpyo_Happyday.print_title_qty;// 수량(title)
begin
  uX := 28;
  uY := 310;
  uHeight := 35;
  uBold := 0;
  uAngle := 0;
  uUnderline := 0;
  uFont_name := 'Arial';
  uContent_1 := '수량';

  windowsfont(uX, uY, uHeight, uAngle, uBold, uUnderline, pChar(uFont_name), pChar(uContent_1));
end;

procedure TCls_Mulpyo_Happyday.print_title_bunch;// 덩이(title)
begin
  uX := 328;
  uY := 310;
  uHeight := 35;
  uBold := 0;
  uAngle := 0;
  uUnderline := 0;
  uFont_name := 'Arial';
  uContent_1 := '덩이';

  windowsfont(uX, uY, uHeight, uAngle, uBold, uUnderline, pChar(uFont_name), pChar(uContent_1));
end;

procedure TCls_Mulpyo_Happyday.print_content_date(fDate: string);//날짜(content)
begin
  uX := 120;
  uY := 32;
  uHeight := 35;
  uBold := 0;
  uAngle := 0;
  uUnderline := 0;
  uFont_name := 'Arial';
  uContent_1 := fDate;

  windowsfont(uX, uY, uHeight, uAngle, uBold, uUnderline, pChar(uFont_name), pChar(uContent_1));
end;

procedure TCls_Mulpyo_Happyday.print_content_company;//물류사(content)
begin
  uX := 440;
  uY := 32;
  uHeight := 40;
  uBold := 0;
  uAngle := 0;
  uUnderline := 0;
  uFont_name := 'Arial';
  uContent_1 := '(주)해피데이';

  windowsfont(uX, uY, uHeight, uAngle, uBold, uUnderline, pChar(uFont_name), pchar(uContent_1));
end;

procedure TCls_Mulpyo_Happyday.Set_contents(fContent: string);
var
  pPos: integer;
begin
  pPos := Pos('/', fContent);
  if pPos > 0 then
  begin
    uContent_1 := Copy(fContent, 1, pPos);
    uContent_2 := Copy(fContent, pPos + 1, 100);
    Exit;
  end;

  pPos := Pos('(', fContent);
  if pPos > 0 then
  begin
    uContent_1 := Copy(fContent, 1, pPos - 1);
    uContent_2 := Copy(fContent, pPos, 100);
    Exit;
  end;

  pPos := Pos('[', fContent);
  if pPos > 0 then
  begin
    uContent_1 := Copy(fContent, 1, pPos - 1);
    uContent_2 := Copy(fContent, pPos, 100);
    Exit;
  end;
end;

procedure TCls_Mulpyo_Happyday.print_content_cust(fCust_name: string);//거래처(content)
var
  pGap_y: integer;
begin
  uX := 35;
  uY := 85;
  uHeight := 90;
  uBold := 2;
  uAngle := 0;
  uUnderline := 0;
  uFont_name := 'Arial';
  uContent_1 := fCust_name;
  uContent_2 := '';
  //내용 길이가 10 이상이면 내용을 2개로 나누어 2줄로 출력 위함
  if Length(uContent_1) > 20 then
  begin
    Set_contents(uContent_1);
  end;

  if uContent_2 = '' then//2번째 라인에 출력할 내용이 없으면
  begin
    pGap_y := 50;//1라인만 출력할 경우에는 세로로 가운데에 찍기 위해. 본래 uY는 좌상단의 y좌표임
    windowsfont(uX, uY + pGap_y, uHeight, uAngle, uBold, uUnderline, pChar(uFont_name), pchar(uContent_1))
  end
  else begin//2번째 라인에 출력할 내용이 있으면
    windowsfont(uX, uY, uHeight, uAngle, uBold, uUnderline, pChar(uFont_name), pchar(uContent_1));
    pGap_y := 85;
    windowsfont(uX, uY + pGap_y, uHeight, uAngle, uBold, uUnderline, pChar(uFont_name), pchar(uContent_2));
  end;
end;

procedure TCls_Mulpyo_Happyday.print_content_qty(fQty: string);//수량(content)
begin
  uX := 180;
  uY := 285;
  uHeight := 100;
  uBold := 2;
  uAngle := 0;
  uUnderline := 0;
  uFont_name := 'HY견고딕';
  uContent_1 := fQty;

  windowsfont(uX, uY, uHeight, uAngle, uBold, uUnderline, pChar(uFont_name), pChar(uContent_1));
end;

procedure TCls_Mulpyo_Happyday.print_content_bunch(fBunch: string);//덩이(content)
begin
  uX := 450;
  uY := 285;
  uHeight := 100;
  uBold := 2;
  uAngle := 0;
  uUnderline := 0;
  uFont_name := 'HY견고딕';
  uContent_1 := fBunch;

  windowsfont(uX, uY, uHeight, uAngle, uBold, uUnderline, pChar(uFont_name), pChar(uContent_1));
end;

procedure TCls_Mulpyo_Happyday.print_content_publisher(fPublisher: string);//출판사(content)
begin
  uX := 760;
  uY := 75;
  uHeight := 35;
  uBold := 2;
  uAngle := 270;
  uUnderline := 0;
  uFont_name := 'Arial';
  uContent_1 := fPublisher;

  windowsfont(uX, uY, uHeight, uAngle, uBold, uUnderline, pChar(uFont_name), pChar(uContent_1));
end;

procedure TCls_Mulpyo_Happyday.print_line_hor_1;
begin
  uX := 20;//left x
  uY := 30;//left y
  uLine_width := 760;//width
  uLine_height := 2;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.print_line_hor_2;
begin
  uX := 20;//left x
  uY := 72;//left y
  uLine_width := 693;//width
  uLine_height := 2;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.print_line_hor_3;
begin
  uX := 20;//left x
  uY := 280;//left y
  uLine_width := 693;//width
  uLine_height := 2;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.print_line_hor_4;
begin
  uX := 20;//left x
  uY := 380;//left y
  uLine_width := 760;//width
  uLine_height := 2;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.print_line_ver_1;
begin
  uX := 20;//left x
  uY := 30;//left y
  uLine_width := 2;//width
  uLine_height := 350;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.print_line_ver_2;
begin
  uX := 90;//left x
  uY := 30;//left y
  uLine_width := 2;//width
  uLine_height := 45;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.print_line_ver_3;
begin
  uX := 90;//left x
  uY := 280;//left y
  uLine_width := 2;//width
  uLine_height := 100;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.print_line_ver_4;
begin
  uX := 320;//left x
  uY := 30;//left y
  uLine_width := 2;//width
  uLine_height := 45;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.print_line_ver_5;
begin
  uX := 320;//left x
  uY := 280;//left y
  uLine_width := 2;//width
  uLine_height := 100;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.print_line_ver_6;
begin
  uX := 385;//left x
  uY := 30;//left y
  uLine_width := 2;//width
  uLine_height := 45;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.print_line_ver_7;
begin
  uX := 385;//left x
  uY := 280;//left y
  uLine_width := 2;//width
  uLine_height := 100;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.print_line_ver_8;
begin
  uX := 710;//left x
  uY := 30;//left y
  uLine_width := 2;//width
  uLine_height := 350;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.print_line_ver_9;
begin
  uX := 780;//left x
  uY := 30;//left y
  uLine_width := 2;//width
  uLine_height := 350;//height

  uCommand := 'BAR ' + IntToStr(uX) + ', ' + IntToStr(uY) + ', ' + IntToStr(uLine_width) + ', ' + IntToStr(uLine_height);
  sendcommand(PChar(uCommand))
end;

procedure TCls_Mulpyo_Happyday.command_open;
begin
  openport(PChar(printer_name));
  clearbuffer;
  sendcommand('DIRECTION 1');
end;

procedure TCls_Mulpyo_Happyday.command_close;
begin
  printlabel('1', '1');
  closeport;
end;

procedure TCls_Mulpyo_Happyday.print_contents(fDate, fCust_name, fQty, fBunch, fPublisher: string);
begin
  // ============ title 부분 출력
  print_title_date;                   // 날짜(title)
  print_title_company;                // 물류사(title)
  print_title_qty;                    // 수량(title)
  print_title_bunch;                  // 덩이(title)
  // ============ content 부분 출력
  print_content_date(fDate);          //날짜(content)
  print_content_company;              //물류사(content)
  print_content_cust(fCust_name);     //거래처(content)
  print_content_qty(fQty);            //수량(content)
  print_content_bunch(fBunch);        //덩이(content)
  print_content_publisher(fPublisher);//출판사(content)
  // ============ 가로선 출력
  print_line_hor_1;
  print_line_hor_2;
  print_line_hor_3;
  print_line_hor_4;
  // ============ 세로선 출력
  print_line_ver_1;
  print_line_ver_2;
  print_line_ver_3;
  print_line_ver_4;
  print_line_ver_5;
  print_line_ver_6;
  print_line_ver_7;
  print_line_ver_8;
  print_line_ver_9;
end;

end.
