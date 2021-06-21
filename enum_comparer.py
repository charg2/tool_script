  
from os import remove
import os;
import copy;



def find_enum( words ):
    if "enum" in words:
        on_find_enum( words );

def find_class( words ):
    if "class" in words:
        on_find_class( words );

def find_left( words ):
    if "{" in words:
        on_find_left( words );

def find_right( words ):
    global current_enum_file_name;
    global current_enum;
    global key; # current_enum_name
    global current_line_num;
    global current_enum_value;

    enum_name = key;
    name      = "";
    is_end    = False;
    has_equal = False;

    # 붙어 있는 경우 ex Max=1,
    first_word = words[ 0 ];

    if "//" in first_word:
        first_word = first_word.split( "//" )[ 0 ];

    if "};" in first_word:
        first_word = first_word.split( "};" )[ 0 ];


    i = 0;
    for word in words:
        if "//" == word[:2]:
            break;

        if "=" in word:
            splited_words = word.split( "=" );
            enum_val_word = splited_words[ 1 ];

            print( current_line_num );

            if "" == enum_val_word:
                enum_val_word = words[ i + 1 ]; # Max = 1,
            if "//" in enum_val_word:
                enum_val_word = enum_val_word.split( "//" )[ 0 ];
            if "," in enum_val_word:
                enum_val_word = enum_val_word.split( "," )[ 0 ];
            if "0x" in enum_val_word:
                current_enum_value = int( enum_val_word, 0 );
            else:
                current_enum_value = int( enum_val_word );
            
        i += 1;

    
    # Max,
    if "," in first_word:
        first_word = first_word.split( "," )[ 0 ];
        name = first_word;
    else:
        name = first_word;

    if "=" in first_word:
       first_word = first_word.split( "=" )[ 0 ];
       name = first_word;
    else:
        name = first_word;

    if name != "":
        current_enum[ name ] = { "name" : name, "value" : current_enum_value, "line" : current_line_num };
        current_enum_value += 1;

    for word in words:
        if "//" in word:
            prefix = word.split( "//" )[ 0 ]; # 주석 뒤는 무시
            if prefix == "":
                return;

        if "};" in word:
            is_end = True;
            on_find_right( words );        
            return;


def on_find_enum( words ):
    for word in words:
        if word == "enum":
            return find_class( words[1:] ); 

def on_find_class( words ):
    global key;
    global current_filter;

    for word in words:
        if word == "class":
            key = words[ 1 ];
            current_filter = find_left;

def on_find_left( words ):
    global current_filter;
    current_filter = find_right;

def on_find_right( words ):
    global current_filter;
    global current_enum;
    global key; #current_enum_name
    global current_enums;
    global current_enum_value;

    current_filter = find_enum;
    current_enums[ key ] = current_enum;
    
    current_enum = {};
    current_enum_value = 0;


def display_enum_list_detail() :
    global enum_files;
    
    for data in enum_files :
        print( data );
        print( enum_files[ data ] );
    print( "-----------------------------------------" );

def display_enum_list() :
    global enum_files;
    
    for key in enum_files.keys() :
        print( key );
    print( "-----------------------------------------" );



def global_display_enum_list_detail():
    global enum_file_dict;
    for enum_file in enum_file_dict.items():
        #print( enum_file );
        
        print( enum_file[0] );
        print( "-----------------------------------------" );
        for enum in enum_file[1].items():
            print( "enum class" + enum[0] );
            print( "{" );
            for val in enum[1].items():
                print( val[1] );
            print( "};" );


        #for enum in enums.keys():
        #    i = 1;
        #    for e in enums[ enum ]:
        #        print( enum + str( i ) + " : " + e );
        #        i += 1;

def global_display_enum_list():
    for file_name in enum_file_dict.keys():
        print( file_name );
        i = 1;
        for enum in enum_file_dict[ file_name ].keys():
            print( str( i ) + " : " + enum );
            i += 1;


def add_file( name ):
    global enum_file_list;
    global enum_file_dict
    global enum_files;
    global current_enums;
    global current_line_num;

    if not enum_file_dict.__contains__( name ):
        enum_file_dict[ name ] = current_enums;
        enum_file_list.append( current_enums );
    else:
        print( "already exist file" );
    
    current_enums       = {};
    current_line_num    = 0;
    enum_files          = {};
    


def display_ui():
    print( "1. new <filename>" );
    print( "2. copy <new_enum_files_name> <target>" );
    print( "3. show" );
    print( "4. sub <left> <right>" );
    print( "5. clear" );
    print( "6. mark <file_name>" );

def input_commands():
    return input().split();

def open_file( file_name ):
    global current_enum_file_name;
    global enum_files;
    
    current_enum_file_name = file_name;

    try:
        file  = open( file_name, mode = 'rt' );
    except FileNotFoundError:
        print(" FileNotFoundError! ");
        return None;
    else:
        return file;
    

def parse_file( file ):
    global current_filter;
    global current_line_num;

    lines    = file.readlines();

    for line in lines:
        current_line_num += 1;

        s = line.split();
        if len( s ) == 0 :
            continue;

        current_filter( s );

def new_file( file_name ):
    file = open_file( file_name );
    if not file:
        return;

    parse_file( file );
    add_file( file_name );

def new_files( file_name_list ):
    for file_name in file_name_list:
        new_file( file_name );

def copy_file( new_enum_files_name, target_key ):
    global enum_file_dict;
    global enum_file_list;

    #if len( keys ) < 2:
    #    print( "keys size less than 2" );

    #new_enum_files_name    = keys[0];
    #target_key = keys[1];

    if enum_file_dict.__contains__( target_key ):
        enum_file_dict[ new_enum_files_name ] = copy.deepcopy( enum_file_dict[ target_key ] );
        enum_file_list.append( enum_file_dict[ new_enum_files_name ] );
    else:
        print( "not exist target_key" );

def sub_file_detail( left, right ):
    global enum_file_dict;
    
    if not enum_file_dict.__contains__( left ) :
        print( "not exist left file" );

    if not enum_file_dict.__contains__( right ) :
        print( "not exist right file" );

    l_file = enum_file_dict[ left  ]; #l enums
    r_file = enum_file_dict[ right ]; #r enums
    
    for r_key in r_file.keys():
        if l_file.__contains__( r_key ): #해당 에넘이 있으면
            l_enum = l_file[ r_key ];
            r_enum = r_file[ r_key ];

            for r_enum_val in r_enum.items():
                if l_enum.__contains__( r_enum_val[0] ):
                    if l_enum[ r_enum_val[0] ][ "name" ] == r_enum_val[ 1 ][ "name" ]:
                        if l_enum[ r_enum_val[0] ][ "value" ] == r_enum_val[ 1 ][ "value" ]:
                            del l_enum[ r_enum_val[0] ];
            #if len( l_file[ r_key ] ) == 0:
            #    del l_file[ r_key ];

def sub_file( left, right ):
    global enum_file_dict;
    
    if not enum_file_dict.__contains__( left ) :
        pritn( "not exist left file" );

    if not enum_file_dict.__contains__( right ) :
        pritn( "not exist right file" );

    l_file = enum_file_dict[ left ];
    r_file = enum_file_dict[ right ];
    for r_key in r_file.keys():
        if l_file.__contains__( r_key ):
            del l_file[ r_key ];

def delete_file( key ):
    global enum_file_dict;
    global enum_file_list;
    
    if not enum_file_dict.__contains__( key ) :
        pritn( "not exist key file" );
    else:
        enum_file_list.remove( enum_file_dict[ key ] );
        del enum_file_dict[ key ];

def delete_enum_file_list( keys ):
    for key in keys:
        delete_file( key );

def mark_enum_value_in_memory( enum_file_name ):
    global enum_file_dict;

    read_file  = open( enum_file_name, mode = 'rt' );
    if not read_file:
        return;

    if not enum_file_dict.__contains__( enum_file_name ):
        print( "파일 음슴" );
        return;

    lines    = read_file.readlines();
    read_file.close();


    enum_file = enum_file_dict[ enum_file_name ];
    for enum in enum_file.items():
        for line_info in enum[ 1 ].values():
            line = line_info[ "line" ];
            print( line );
            lines[ line -1 ] = diff_marker + lines[ line -1 ];

    w_file  = open( enum_file_name, mode = 'wt' );
    if not w_file:
        return;

    w_file.writelines( lines );
    





def over_wirte_file():
    pass;


def execute( cmds ):
    if len( cmds ) == 0:
        return;

    if cmds[ 0 ] == "new":
        new_file( cmds[ 1 ] );
    elif cmds[ 0 ] == "new_list":
        new_files( cmds[ 1: ] );
    elif cmds[ 0 ] == "delete":
        delete_file( cmds[ 1 ] );
    elif cmds[ 0 ] == "delete_list":
        delete_enum_file_list( cmds[ 1: ] );
    elif cmds[ 0 ] == "copy":
        copy_file( cmds[ 1 ], cmds[2] );
    elif cmds[ 0 ] == "sub":
        sub_file( cmds[1], cmds[2] );
    elif cmds[ 0 ] == "sub_detail":
        sub_file_detail( cmds[1], cmds[2] );
    elif cmds[ 0 ] == "show":
        global_display_enum_list();
    elif cmds[ 0 ] == "show_detail":
        global_display_enum_list_detail();
    elif cmds[ 0 ] == "clear":
        os.system('cls');
    elif cmds[ 0 ] == "mark":
        mark_enum_value_in_memory( cmds[1] );

def initiliaze():
    cmds_executor = {};    
    cmds_executor[ "clear"       ] = lambda : os.system('cls');
    cmds_executor[ "copy"        ] = copy_file;
    cmds_executor[ "delete"      ] = delete_file;
    cmds_executor[ "delete_list" ] = delete_enum_file_list;
    cmds_executor[ "new"         ] = new_file;
    cmds_executor[ "new_list"    ] = new_enum_file_list;
    cmds_executor[ "show"        ] = global_display_enum_list;
    cmds_executor[ "show_detail" ] = global_display_enum_list_detail;
    cmds_executor[ "sub"         ] = sub_file;
    cmds_executor[ "sub_detail"  ] = sub_file_detail;

    return cmds_executor;


current_enum_file_name  = "";
current_enum            = {}; # 현재 파시중인 enum
current_enums           = {}; # 현재 파시중인 enums
current_enum_value      = 0;

current_filter          = find_enum;
current_line_num        = 0;

enum_files              = {};
enum_file_dict          = {};
enum_file_list          = [];
key                     = "";

diff_marker             = "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<";

def main():
    while True:
        display_ui();
        cmds = input_commands();
        execute( cmds );

main();
