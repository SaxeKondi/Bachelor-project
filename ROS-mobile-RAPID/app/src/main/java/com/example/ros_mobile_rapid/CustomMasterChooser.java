package com.example.ros_mobile_rapid;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;


import androidx.appcompat.app.AppCompatActivity;

import org.ros.internal.node.client.MasterClient;
import org.ros.internal.node.xmlrpc.XmlRpcTimeoutException;
import org.ros.namespace.GraphName;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.Locale;
import java.util.regex.Pattern;

public class CustomMasterChooser extends AppCompatActivity {
    private static final int DEFAULT_PORT = 11311;
    private EditText Master_URI;
    private Button connectButton;
    public static final String MASTER_URI = "com.example.umarosandroid.MASTER_URI";
    private static final String CONNECTION_EXCEPTION_TEXT = "ECONNREFUSED";
    private static final String UNKNOW_HOST_TEXT = "UnknownHost";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup);

        final Pattern uriPattern = RosURIPattern.URI;

        Master_URI = findViewById(R.id.master_ip);
        connectButton = findViewById(R.id.connect_button);
        Master_URI.addTextChangedListener(new TextWatcher() {
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                final String uri = "http://" + s.toString();
                if(!uriPattern.matcher(uri).matches()) {
                    Master_URI.setError("Please enter valid URI");
                    connectButton.setEnabled(false);
                }
                else {
                    Master_URI.setError(null);
                    connectButton.setEnabled(true);
                }
            }

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void afterTextChanged(Editable s) {
            }
        });
        connectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String tmpURI = "http://" + Master_URI.getText().toString();

                // Check to see if the URI has a port.
                final Pattern portPattern = RosURIPattern.PORT;
                if(!portPattern.matcher(tmpURI).find()) {
                    // Append the default port to the URI and update the TextView.
                    tmpURI = String.format(Locale.getDefault(),"%s:%d/",tmpURI,DEFAULT_PORT);
                }

                // Set the URI for connection.
                final String uri = tmpURI;

                // Prevent further edits while we verify the URI.
                // Note: This was placed after the URI port check due to odd behavior
                // with setting the connectButton to disabled.
                Master_URI.setEnabled(false);
                connectButton.setEnabled(false);

                // Make sure the URI can be parsed correctly and that the master is
                // reachable.
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        boolean result;

                        try {
                            MasterClient masterClient = new MasterClient(new URI(uri));
                            masterClient.getUri(GraphName.of("android/master_chooser_activity"));
                            toast("Connected!");
                            findViewById(R.id.Disconnected_text).setVisibility(View.INVISIBLE);
                            findViewById(R.id.Connected_text).setVisibility(View.VISIBLE);
                            result = true;
                        } catch (URISyntaxException e) {
                            toast("Invalid URI.");
                            result = false;
                        } catch (XmlRpcTimeoutException e) {
                            toast("Master unreachable!");
                            result = false;
                        }
                        catch (Exception e) {
                            String exceptionMessage = e.getMessage();
                            if(exceptionMessage.contains(CONNECTION_EXCEPTION_TEXT))
                                toast("Unable to communicate with master!");
                            else if(exceptionMessage.contains(UNKNOW_HOST_TEXT))
                                toast("Unable to resolve URI hostname!");
                            else
                                toast("Communication error!");
                            result = false;
                        }


                        if (result) {
                            //Update Recent Master URI

                            // If the displayed URI is valid then pack that into the intent.
                            // Package the intent to be consumed by the calling activity.
                            Intent mIntent = new Intent(CustomMasterChooser.this, MainActivity.class);
                            mIntent.putExtra(MASTER_URI,uri);

                            //mIntent.putExtra(ENABLE_NLP,enableNlp);
                            startActivity(mIntent);
                            setResult(RESULT_OK, mIntent);

                        } else {
                            connectButton.setEnabled(true);
                            Master_URI.setEnabled(true);
                        }
                    }
                });
            }
        });
        }

        @Override
        protected void onStart(){
        super.onStart();
            Master_URI.setEnabled(true);
            connectButton.setEnabled(true);
            findViewById(R.id.Disconnected_text).setVisibility(View.VISIBLE);
            findViewById(R.id.Connected_text).setVisibility(View.INVISIBLE);

        }

    protected void toast(final String text) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                Toast.makeText(CustomMasterChooser.this, text, Toast.LENGTH_SHORT).show();
            }
        });
    }

    @Override
    public void onBackPressed() {
        //Prevent user from going back to Launcher Activity since no Master is connected.
        this.moveTaskToBack(true);
    }

private static class RosURIPattern
{
    /* A word boundary or end of input.  This is to stop foo.sure from matching as foo.su */
    private static final String WORD_BOUNDARY = "(?:\\b|$|^)";

    /**
     * Valid UCS characters defined in RFC 3987. Excludes space characters.
     */
    private static final String UCS_CHAR = "[" +
            "\u00A0-\uD7FF" +
            "\uF900-\uFDCF" +
            "\uFDF0-\uFFEF" +
            "\uD800\uDC00-\uD83F\uDFFD" +
            "\uD840\uDC00-\uD87F\uDFFD" +
            "\uD880\uDC00-\uD8BF\uDFFD" +
            "\uD8C0\uDC00-\uD8FF\uDFFD" +
            "\uD900\uDC00-\uD93F\uDFFD" +
            "\uD940\uDC00-\uD97F\uDFFD" +
            "\uD980\uDC00-\uD9BF\uDFFD" +
            "\uD9C0\uDC00-\uD9FF\uDFFD" +
            "\uDA00\uDC00-\uDA3F\uDFFD" +
            "\uDA40\uDC00-\uDA7F\uDFFD" +
            "\uDA80\uDC00-\uDABF\uDFFD" +
            "\uDAC0\uDC00-\uDAFF\uDFFD" +
            "\uDB00\uDC00-\uDB3F\uDFFD" +
            "\uDB44\uDC00-\uDB7F\uDFFD" +
            "&&[^\u00A0[\u2000-\u200A]\u2028\u2029\u202F\u3000]]";

    /**
     * Valid characters for IRI label defined in RFC 3987.
     */
    private static final String LABEL_CHAR = "a-zA-Z0-9" + UCS_CHAR;

    /**
     * RFC 1035 Section 2.3.4 limits the labels to a maximum 63 octets.
     */
    private static final String IRI_LABEL =
            "[" + LABEL_CHAR + "](?:[" + LABEL_CHAR + "\\-]{0,61}[" + LABEL_CHAR + "]){0,1}";

    private static final Pattern IP_ADDRESS
            = Pattern.compile(
            "((25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9])\\.(25[0-5]|2[0-4]"
                    + "[0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9]|0)\\.(25[0-5]|2[0-4][0-9]|[0-1]"
                    + "[0-9]{2}|[1-9][0-9]|[1-9]|0)\\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}"
                    + "|[1-9][0-9]|[0-9]))");

    /**
     * Regular expression that matches domain names without a TLD
     */
    private static final String RELAXED_DOMAIN_NAME =
            "(?:" + "(?:" + IRI_LABEL + "(?:\\.(?=\\S))" +"?)+" +
                    "|" + IP_ADDRESS + ")";

    private static final String HTTP_PROTOCOL = "(?i:http):\\/\\/";

    public static final int HTTP_PROTOCOL_LENGTH = ("http://").length();

    private static final String PORT_NUMBER = "\\:\\d{1,5}\\/?";

    /**
     *  Regular expression pattern to match valid rosmaster URIs.
     *  This assumes the port number and trailing "/" will be auto
     *  populated (default port: 11311) if left out.
     */
    public static final Pattern URI = Pattern.compile("("
            + WORD_BOUNDARY
            + "(?:"
            + "(?:" + HTTP_PROTOCOL + ")"
            + "(?:" + RELAXED_DOMAIN_NAME + ")"
            + "(?:" + PORT_NUMBER + ")?"
            + ")"
            + WORD_BOUNDARY
            + ")");

    public static final Pattern PORT = Pattern.compile(PORT_NUMBER);
}
}