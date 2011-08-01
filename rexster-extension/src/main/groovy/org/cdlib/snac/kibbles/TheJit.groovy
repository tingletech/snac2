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
import javax.ws.rs.core.Response;

@ExtensionNaming(namespace = "snac", name = "theJit")
public class TheJit extends AbstractRexsterExtension {

    static {
        Gremlin.load();
    }

    @ExtensionDefinition(extensionPoint = ExtensionPoint.VERTEX)
    @ExtensionDescriptor(description = "JSON needed for graphs in the JavaScript InfoVis Toolkit")
    public ExtensionResponse evaluate(@RexsterContext RexsterResourceContext context,
                                      @RexsterContext Vertex v) {

        JSONArray output = new JSONArray();

        def counter = 0;
        // first; build up the nodes that will show up on the graph
        def neighbors = [];

        // using a for loop because that is the only thing you can break out of
        for( def vertex : v.both.uniqueObject().sort{-it.score}) {
            counter ++; if (counter > 50) { break; }
            vertex._().aggregate(neighbors)>>-1;
        }

        output.put(buildNode(v, neighbors));

        // now; gotta loop through the first 50 again        
        counter = 0;
        for( def vertex : v.both.uniqueObject().sort{-it.score}) {
            counter ++; if (counter > 50) { break; }
            output.put(buildNode(vertex, neighbors));
        }

        // return the results
        return new ExtensionResponse(Response.ok(output).build());
    }

    // build array of adjacent nodes
    private buildAdjacencies(vertex, neighbors) {
          JSONArray collect = new JSONArray();
          def self = [];
          vertex._().aggregate(self)>>-1;
          vertex.bothE.bothV.uniqueObject().retain(neighbors).except(self).each {
            collect.put(it.id as String);
          };
          return collect;
    }

    // build the JSON for the node
    private buildNode(vertex, neighbors) {
            def node = new JSONObject();
            node.put("id", vertex.id as String);
            node.put("name", vertex.identity);
            node.put("adjacencies", buildAdjacencies(vertex, neighbors));
            return node;
    }
}
