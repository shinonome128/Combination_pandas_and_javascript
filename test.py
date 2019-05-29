"""
Load module
"""
import pandas as pd
import sys
import os
import glob
import configparser
# import pdb; pdb.set_trace()


"""
Main Process
"""
def main():

    # Get parms from config file
    config_file = configparser.ConfigParser()
    config_file.read('./test.conf', 'UTF-8')
    input_file = config_file.get('control','INPUT_FILE')
    output_dir = config_file.get('control','OUTPUT_DIR')
    max_entry = int(config_file.get('control','MAX_ENTRY'))
    labels = config_file.get('interface','LABELS').split(',')

    # Make html template
    html_template = """
    <!doctype html>
    <html lang="ja">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
        <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
      </head>
      <body>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
        <script type="text/javascript" src="../test.js"></script>
        <div class="container">
            {table}
            <br>
            {textarea}
            <br>
            {button}
        </div>
      </body>
    </html>
    """

    # Make select html
    str1 = '<select style="width: 220px" class="form-control">'
    str2 = ''
    for i in labels:
        line = '<option value=' + '"' + i + '">' + i + '</option>'
        str2 = str2 + line
    str3 = '</select>'
    html_select = str1 + str2 + str3

    # Make text area html
    html_textarea= "<div class=\"form-group\"> <label for=\"exampleFormControlTextarea1\">result_text_form</label><textarea class=\"form-control\" id=\"exampleFormControlTextarea1\" rows=\"3\"></textarea></div>"

    # Make button html
    html_button= "<button type=\"button\" onClick=\"buttonClick()\" class=\"btn btn-primary\">create_result</button>"

    # Make all dataframe
    df = pd.read_csv(input_file, names=["path", "name1"],sep='\t')
    pd.set_option("display.max_colwidth", 1000)
    df['image'] = df["path"].map(lambda s: "<img src='../{}'  width='200' />".format(s))
    df['check'] = html_select
    df = df.loc[:,['path','name1','image','check']]

    # Make result file for each label
    for i in labels:

        # Make data frame for each label
        df_i = df.query('name1 == @i')
        df_i.reset_index(drop=True, inplace=True)

        # Check dataframe length, if datasize is larger than max entry in config file, split html files
        if len(df_i) >= max_entry:

            for j in range(0, len(df_i), max_entry):

                # Split html files
                table = df_i[j:j+max_entry].to_html(classes=["table", "table-bordered", "table-hover"], escape=False)
                # Make html file
                html = html_template.format(table=table,textarea=html_textarea,button=html_button)
                with open(output_dir +"/" + i + "_" + str(j) + ".html", "w") as f:
                    f.write(html)

        else:
            # Make table html
            table = df_i.to_html(classes=["table", "table-bordered", "table-hover"], escape=False)

            # Make html file
            html = html_template.format(table=table,textarea=html_textarea,button=html_button)
            with open(output_dir +"/" + i + ".html", "w") as f:
                f.write(html)



    # Make other dataframe and html file
    df_other = df.query('name1 != @labels')
    df_other.reset_index(drop=True, inplace=True)

    if len(df_other) >= max_entry:
        for i in range(0, len(df_other), max_entry):
            # Split html files
            table = df_other[i:i+max_entry].to_html(classes=["table", "table-bordered", "table-hover"], escape=False)
            # Make html file
            html = html_template.format(table=table,textarea=html_textarea,button=html_button)
            with open(output_dir +"/OTHER" + "_" + str(i) + ".html", "w") as f:
                f.write(html)

    else:
        # Make table html
        table = df_other.to_html(classes=["table", "table-bordered", "table-hover"], escape=False)
        html = html_template.format(table=table,textarea=html_textarea,button=html_button)
        with open(output_dir + "/OTHER.html", "w") as f:
            f.write(html)


"""
This script is not executed when called from outside
"""
if __name__ == "__main__":
    main()