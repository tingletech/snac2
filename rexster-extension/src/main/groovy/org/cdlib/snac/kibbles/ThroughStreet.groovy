package org.cdlib.snac.kibbles;

import com.tinkerpop.blueprints.pgm.Edge;
import com.tinkerpop.blueprints.pgm.Graph;
import com.tinkerpop.blueprints.pgm.Vertex;
import com.tinkerpop.rexster.extension.*;
import com.tinkerpop.rexster.RexsterResourceContext;
import org.codehaus.jettison.json.JSONObject;
import org.codehaus.jettison.json.JSONArray;
import com.tinkerpop.blueprints.pgm.util.json.JSONWriter;
import com.tinkerpop.gremlin.Gremlin;

@ExtensionNaming(namespace = "snac", name = "mostAssociated")
public class ThroughStreet extends AbstractRexsterExtension {

    static {
        Gremlin.load();
    }

    @ExtensionDefinition(extensionPoint = ExtensionPoint.VERTEX)
    @ExtensionDescriptor(description = "JSON needed for a most associated javascript visualization page")
    public ExtensionResponse evaluate(@RexsterContext RexsterResourceContext context,
                                      @RexsterContext Vertex v) {

        // properties to pull out of database
        def properties = ['identity','entityType','score']

        // hold the JSON output
        JSONObject result = new JSONObject();
        // hold the neighbors
        JSONArray associatedWith = new JSONArray();
        JSONArray correspondedWith = new JSONArray();

        // put information for the center vertex
        result.put("this", JSONWriter.createJSONElement(v));

        // put counts of neighbors
        result.put("correspondedWithCount", v.out('correspondedWith').uniqueObject().count());
        result.put("associatedWithCount", v.out('associatedWith').uniqueObject().count());

        // snac schema change:
        // for (z in g.V ) { z.score = z.out.count() }  <-- add a new pre-computation
        // need to add this pre-computation to the graph generation process

        // get the first 50 most "popular" correspondents 
        def counter = 0;
        for( 
            def vertex : 
            v.out('correspondedWith').uniqueObject().sort{-it.score}
        ) { 
            counter ++; if (counter > 50) { break; } 
            correspondedWith.put(JSONWriter.createJSONElement(vertex,properties,false));
        }

        // get the first 50 most "popular" associated names
        counter = 0;
        for( 
            def vertex : 
            // v.out('associatedWith').unique().sort{it.out.count()}.reverse() 
            v.out('associatedWith').uniqueObject().sort{-it.score} 
        ) { 
            counter ++; if (counter > 50) { break; } 
            associatedWith.put(JSONWriter.createJSONElement(vertex,properties,false));
        }

        // put the neighbors
        result.put("correspondedWith", correspondedWith);
        result.put("associatedWith", associatedWith);

        // return the results
        return ExtensionResponse.ok(result);
    }
}
