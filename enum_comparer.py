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
    global key;
    global datas;

    if "};" in words:
        on_find_right( words );
        return;
    
    word = words[ 0 ];
    if "=" in word:
        word = word.split( "=" )[ 0 ];

    if "," in word:
        word = word.split( "," )[ 0 ];

    if datas.__contains__( key ) :
        datas[ key ].add( word );
    else:
        datas[ key ] = { word };

def on_find_enum( words ):
    for word in words:
        words.remove( word )
        if word == "enum":
            return find_class( words ); 

def on_find_class( words ):
    global key;
    global current_filter;

    for word in words:
        words.remove( word )
        if word == "class":
            key = words[ 0 ];
            current_filter = find_left;

def on_find_left( words ):
    global current_filter;
    current_filter = find_right;

def on_find_right( words ):
    global current_filter;

    current_filter = find_enum;



def display_enum_list_detail() :
    global datas;
    
    for data in datas :
        print( data );
        print( datas[ data ] );
    print( "-----------------------------------------" );

def display_enum_list() :
    global datas;
    
    for key in datas.keys() :
        print( key );
    print( "-----------------------------------------" );

key = "";
current_filter = find_enum;
datas = {};
file_dict = {};
file_list = [];


def global_display_enum_list_detail():
    global file_dict;
    for file_name in file_dict.keys():
        print( file_name );
        enums = file_dict[ file_name ];
        for enum in enums.keys():
            i = 1;
            for e in enums[ enum ]:
                print( str( i ) + " : " + e );
                i += 1;

def global_display_enum_list():
    for file_name in file_dict.keys():
        print( file_name );
        i = 1;
        for enum in file_dict[ file_name ].keys():
            print( str( i ) + " : " + enum );
            i += 1;

def add_file( name ):
    global file_list;
    global file_dict
    global datas;

    if not file_dict.__contains__( name ):
        file_dict[ name ] = datas;
        file_list.append( datas );
    else:
        print( "already exist file" );
    
    datas = {};


def display_ui():
    print( "1. new <filename>" );
    print( "2. copy <new_key> <target>" );
    print( "3. show" );
    print( "4. sub <left> <right>" );
    print( "5. clear" );

def input_commands():
    return input().split();

def open_file( file_name ):
    try:
        file  = open( file_name, mode = 'rt' );
    except FileNotFoundError:
        print(" FileNotFoundError! ");
        return None;
    else:
        return file;
    

def parse_file( file ):
    global current_filter;

    lines = file.readlines();
    
    for line in lines:
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

def copy_file( new_key, target_key ):
    global file_dict;
    global file_list;

    #if len( keys ) < 2:
    #    print( "keys size less than 2" );

    #new_key    = keys[0];
    #target_key = keys[1];

    if file_dict.__contains__( target_key ):
        file_dict[ new_key ] = copy.deepcopy( file_dict[ target_key ] );
        file_list.append( file_dict[ new_key ] );
    else:
        print( "not exist target_key" );

def sub_file_detail( left, right ):
    global file_dict;
    
    if not file_dict.__contains__( left ) :
        pritn( "not exist left file" );

    if not file_dict.__contains__( right ) :
        pritn( "not exist right file" );

    l_file = file_dict[ left ];
    r_file = file_dict[ right ];
    for r_key in r_file.keys():
        if l_file.__contains__( r_key ):
            l_file[ r_key ] -= r_file[ r_key ];
            if len( l_file[ r_key ] ) == 0:
                del l_file[ r_key ];

def sub_file( left, right ):
    global file_dict;
    
    if not file_dict.__contains__( left ) :
        pritn( "not exist left file" );

    if not file_dict.__contains__( right ) :
        pritn( "not exist right file" );

    l_file = file_dict[ left ];
    r_file = file_dict[ right ];
    for r_key in r_file.keys():
        if l_file.__contains__( r_key ):
            del l_file[ r_key ];

def delete_file( key ):
    global file_dict;
    global file_list;
    
    if not file_dict.__contains__( key ) :
        pritn( "not exist key file" );
    else:
        file_list.remove( file_dict[ key ] );
        del file_dict[ key ];

def delete_file_list( keys ):
    for key in keys:
        delete_file( key );

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
        delete_file_list( cmds[ 1: ] );
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

def initiliaze():
    cmds_executor = {};    
    cmds_executor[ "clear"       ] = lambda : os.system('cls');
    cmds_executor[ "copy"        ] = copy_file;
    cmds_executor[ "delete"      ] = delete_file;
    cmds_executor[ "delete_list" ] = delete_file_list;
    cmds_executor[ "new"         ] = new_file;
    cmds_executor[ "new_list"    ] = new_file_list;
    cmds_executor[ "show"        ] = global_display_enum_list;
    cmds_executor[ "show_detail" ] = global_display_enum_list_detail;
    cmds_executor[ "sub"         ] = sub_file;
    cmds_executor[ "sub_detail"  ] = sub_file_detail;

    return cmds_executor;

def main():
    while True:
        display_ui();
        cmds = input_commands();
        execute( cmds );

main();
